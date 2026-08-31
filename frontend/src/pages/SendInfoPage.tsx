import {
  AlertCircle,
  Check,
  CheckCircle2,
  Eye,
  FileCheck,
  FileText,
  History,
  Info,
  Mail,
  Paperclip,
  Send,
  ShieldCheck,
  Trash2,
  Trophy,
  UploadCloud,
  Users,
} from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";
import type { ChangeEvent, FormEvent } from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { Page, PortalShell } from "../components/UI";
import { managementSidebar, sidebar } from "../data/platform";
import { apiRequest } from "../lib/api";
import { showToast } from "../lib/toast";

type TournamentOption = {
  slug: string;
  name: string;
  sport: string;
  location?: string;
  status?: string;
};

type Recipient = {
  id: string;
  email: string;
  captain_name: string;
  team_name: string;
  team_code: string;
  payment_status: string;
};

type BroadcastEvent = {
  id: string;
  tournament_slug: string;
  audience: string;
  message: string;
  created_at: string;
  status: string;
};

export function SendInfoPage({ role = "management" }: { role?: "admin" | "management" }) {
  const { token, user } = useAuth();
  const location = useLocation();
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [tournaments, setTournaments] = useState<TournamentOption[]>([]);
  const [selectedTournament, setSelectedTournament] = useState<string>("");
  const [loadingTournaments, setLoadingTournaments] = useState(false);

  // Recipient info
  const [recipients, setRecipients] = useState<Recipient[]>([]);
  const [loadingRecipients, setLoadingRecipients] = useState(false);
  const [showRecipientsList, setShowRecipientsList] = useState(false);

  // Form states
  const [subject, setSubject] = useState("");
  const [content, setContent] = useState("");
  const [attachedFile, setAttachedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  // Preview & Confirm
  const [showPreview, setShowPreview] = useState(false);
  const [confirmModalOpen, setConfirmModalOpen] = useState(false);
  const [sending, setSending] = useState(false);

  // History
  const [history, setHistory] = useState<BroadcastEvent[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  // Load available tournaments
  const loadTournaments = useCallback(async () => {
    if (!token) return;
    setLoadingTournaments(true);
    try {
      const endpoint = role === "admin" || user?.role === "super_admin" ? "/public/tournaments" : "/management/tournaments";
      let data = await apiRequest<TournamentOption[]>(endpoint, { silent: true }, token).catch(() => null);
      if (!Array.isArray(data) || data.length === 0) {
        data = await apiRequest<TournamentOption[]>("/public/tournaments", { silent: true }, token).catch(() => null);
      }
      if (Array.isArray(data)) {
        setTournaments(data);
        if (data.length > 0 && !selectedTournament) {
          setSelectedTournament(data[0].slug);
        }
      }
    } catch {
      // Fallback
    } finally {
      setLoadingTournaments(false);
    }
  }, [token, role, user?.role, selectedTournament]);


  useEffect(() => {
    loadTournaments();
  }, [loadTournaments]);

  // Load recipients for selected tournament
  const loadRecipients = useCallback(async (slug: string) => {
    if (!slug || !token) return;
    setLoadingRecipients(true);
    try {
      const res = await apiRequest<{ tournament: any; count: number; recipients: Recipient[] }>(
        `/management/tournaments/${slug}/recipients`,
        { silent: true },
        token
      );
      if (res?.recipients) {
        setRecipients(res.recipients);
      } else {
        setRecipients([]);
      }
    } catch {
      setRecipients([]);
    } finally {
      setLoadingRecipients(false);
    }
  }, [token]);

  // Load broadcast history
  const loadHistory = useCallback(async (slug: string) => {
    if (!token) return;
    setLoadingHistory(true);
    try {
      const res = await apiRequest<BroadcastEvent[]>(
        `/management/broadcast-history${slug ? `?tournament_slug=${slug}` : ""}`,
        { silent: true },
        token
      );
      if (Array.isArray(res)) {
        setHistory(res);
      }
    } catch {
      // Ignore
    } finally {
      setLoadingHistory(false);
    }
  }, [token]);

  useEffect(() => {
    if (selectedTournament) {
      loadRecipients(selectedTournament);
      loadHistory(selectedTournament);
    }
  }, [selectedTournament, loadRecipients, loadHistory]);

  // Handle file select
  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      setAttachedFile(file);
    }
  }

  function handleDrop(event: React.DragEvent) {
    event.preventDefault();
    setIsDragging(false);
    if (event.dataTransfer.files && event.dataTransfer.files[0]) {
      setAttachedFile(event.dataTransfer.files[0]);
    }
  }

  function removeFile() {
    setAttachedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }

  // Pre-validate and open confirmation modal
  function handleFormSubmit(event: FormEvent) {
    event.preventDefault();
    if (!selectedTournament) {
      showToast("warning", "Tournament Required", "Please select a tournament.");
      return;
    }
    if (!subject.trim()) {
      showToast("warning", "Subject Required", "Please enter an email subject line.");
      return;
    }
    if (!content.trim()) {
      showToast("warning", "Message Content Required", "Please enter your message body.");
      return;
    }
    if (recipients.length === 0) {
      showToast("warning", "No Recipients", "There are no payment-verified participants for this tournament.");
      return;
    }
    setConfirmModalOpen(true);
  }

  // Execute broadcast send
  async function executeBroadcast() {
    if (!token || !selectedTournament) return;
    setSending(true);
    try {
      const formData = new FormData();
      formData.append("tournament_slug", selectedTournament);
      formData.append("subject", subject.trim());
      formData.append("content", content.trim());
      if (attachedFile) {
        formData.append("attachment", attachedFile);
      }

      const response = await fetch("/api/v1/management/send-info", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const result = await response.json();
      if (!response.ok || !result.success) {
        throw new Error(result.message || "Failed to dispatch broadcast email.");
      }

      showToast("success", "Broadcast Dispatched", `Successfully sent email to ${result.data.total_sent} verified participants.`);
      setSubject("");
      setContent("");
      removeFile();
      setConfirmModalOpen(false);
      loadHistory(selectedTournament);
    } catch (caught) {
      showToast("error", "Broadcast Failed", caught instanceof Error ? caught.message : "Could not send broadcast email.");
    } finally {
      setSending(false);
    }
  }

  const activeTournamentObj = tournaments.find((t) => t.slug === selectedTournament);
  const portalSidebar = location.pathname.startsWith("/admin") ? sidebar : managementSidebar;
  const dashboardPath = role === "admin" || user?.role === "super_admin" ? "/admin/dashboard" : "/management/dashboard";

  return (
    <Page>
      <PortalShell
        title="Send Info & Broadcast"
        subtitle="Send announcements, fixtures, schedules, and PDF documents directly to payment-verified participants."
        sidebar={portalSidebar}
        action={<Link className="btn btn-primary" to={dashboardPath}>Dashboard</Link>}
      >
        <div className="send-info-container">
          {/* Main Layout Grid */}
          <div className="send-info-grid">
            {/* Left Column: Compose Form */}
            <div className="panel" style={{ padding: "26px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "18px" }}>
                <Mail size={24} style={{ color: "var(--primary-dark)" }} />
                <h2 style={{ margin: 0, fontSize: "20px" }}>Compose Tournament Broadcast</h2>
              </div>

              <form className="send-info-form" onSubmit={handleFormSubmit}>
                {/* 1. Tournament Selector */}
                <label>
                  Select Tournament
                  <select
                    value={selectedTournament}
                    onChange={(e) => setSelectedTournament(e.target.value)}
                    disabled={loadingTournaments}
                    required
                  >
                    {tournaments.map((t) => (
                      <option key={t.slug} value={t.slug}>
                        {t.name} ({t.sport}{t.location ? ` - ${t.location}` : ""})
                      </option>
                    ))}
                  </select>
                </label>

                {/* Audience / Verified Participant Indicator */}
                <div style={{ background: "#f8fafc", padding: "14px 16px", borderRadius: "12px", border: "1px solid #e2e8f0" }}>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "10px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <Users size={18} style={{ color: "var(--primary)" }} />
                      <span style={{ fontSize: "14px", fontWeight: 700, color: "#0f172a" }}>Target Audience:</span>
                    </div>
                    {loadingRecipients ? (
                      <span style={{ fontSize: "13px", color: "var(--muted)" }}>Checking participants...</span>
                    ) : (
                      <span className="audience-verified-badge">
                        <CheckCircle2 size={16} />
                        {recipients.length} Payment-Verified {recipients.length === 1 ? "Team" : "Teams"}
                      </span>
                    )}
                  </div>

                  <p style={{ margin: "8px 0 0", fontSize: "12px", color: "#64748b", lineHeight: 1.4 }}>
                    <ShieldCheck size={14} style={{ display: "inline", verticalAlign: "text-bottom", color: "var(--primary)" }} /> Emails will be sent <strong>strictly to participants whose registration payment has been verified</strong>.
                  </p>

                  {recipients.length > 0 && (
                    <div style={{ marginTop: "10px" }}>
                      <button
                        type="button"
                        className="btn btn-secondary btn-sm"
                        style={{ fontSize: "12px", padding: "4px 10px" }}
                        onClick={() => setShowRecipientsList(!showRecipientsList)}
                      >
                        {showRecipientsList ? "Hide Recipient List" : `View ${recipients.length} Recipients`}
                      </button>

                      {showRecipientsList && (
                        <div className="recipient-list-chip-row">
                          {recipients.map((r) => (
                            <span key={r.id} className="recipient-chip">
                              <strong>{r.team_name}</strong> ({r.captain_name || r.email})
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* 2. Subject Line */}
                <label>
                  Email Subject Line
                  <input
                    type="text"
                    required
                    placeholder="e.g. Tournament Fixtures, Reporting Times & Schedule Update"
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                  />
                </label>

                {/* 3. Message Content */}
                <label>
                  Message Content (Body)
                  <textarea
                    required
                    placeholder="Type your official announcement, reporting guidelines, match rules, or schedule details here..."
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                  />
                </label>

                {/* 4. PDF Attachment Upload */}
                <div>
                  <label style={{ marginBottom: "6px" }}>Attach Document (PDF, Guidelines, Schedule)</label>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,.png,.jpg,.jpeg,.doc,.docx"
                    style={{ display: "none" }}
                    onChange={handleFileChange}
                  />

                  {!attachedFile ? (
                    <div
                      className={`file-upload-dropzone ${isDragging ? "dragover" : ""}`}
                      onDragOver={(e) => {
                        e.preventDefault();
                        setIsDragging(true);
                      }}
                      onDragLeave={() => setIsDragging(false)}
                      onDrop={handleDrop}
                      onClick={() => fileInputRef.current?.click()}
                    >
                      <UploadCloud size={36} style={{ color: "var(--primary)", margin: "0 auto 8px" }} />
                      <p style={{ margin: 0, fontWeight: 700, fontSize: "14px", color: "#1e293b" }}>
                        Click to upload or drag &amp; drop PDF document
                      </p>
                      <small style={{ color: "#64748b" }}>Supports PDF, Images, or Documents (up to 20MB)</small>
                    </div>
                  ) : (
                    <div className="file-upload-preview">
                      <div className="file-upload-preview-info">
                        <FileCheck size={24} />
                        <div>
                          <span>{attachedFile.name}</span>
                          <small>({(attachedFile.size / 1024).toFixed(1)} KB)</small>
                        </div>
                      </div>
                      <button
                        type="button"
                        className="btn-danger-soft"
                        style={{ padding: "6px 10px", borderRadius: "8px" }}
                        onClick={removeFile}
                        title="Remove file"
                      >
                        <Trash2 size={15} /> Remove
                      </button>
                    </div>
                  )}
                </div>

                {/* Submit Actions */}
                <div style={{ display: "flex", gap: "12px", marginTop: "12px", alignItems: "center" }}>
                  <button
                    className="btn btn-primary"
                    type="submit"
                    disabled={sending || recipients.length === 0}
                    style={{ display: "flex", alignItems: "center", gap: "8px" }}
                  >
                    <Send size={16} /> Send Broadcast to {recipients.length} Participants
                  </button>

                  <button
                    className="btn btn-secondary"
                    type="button"
                    onClick={() => setShowPreview(!showPreview)}
                    style={{ display: "flex", alignItems: "center", gap: "8px" }}
                  >
                    <Eye size={16} /> {showPreview ? "Hide Preview" : "Preview Email"}
                  </button>
                </div>
              </form>
            </div>

            {/* Right Column: Live Email Preview & Guidelines */}
            <div style={{ display: "grid", gap: "20px" }}>
              {/* Preview Box */}
              <div className="email-live-preview-box">
                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "12px" }}>
                  <Eye size={18} style={{ color: "var(--primary)" }} />
                  <strong style={{ fontSize: "15px", color: "#0f172a" }}>Live Email Preview</strong>
                </div>

                <div className="email-live-preview-header">
                  <h3>SMART SPORTZ</h3>
                  <small>Tournament Update &bull; {activeTournamentObj?.name || "Selected Tournament"}</small>
                </div>

                <div style={{ fontSize: "13px", color: "#475569", marginBottom: "12px", borderBottom: "1px solid #f1f5f9", paddingBottom: "8px" }}>
                  <strong>Subject:</strong> {subject || "Tournament Update"}
                </div>

                <div className="email-live-preview-body">
                  <p style={{ margin: "0 0 10px", color: "#64748b" }}>
                    Hello <strong>Captain Name</strong> (Team Name),
                  </p>
                  {content ? (
                    content.split("\n").map((line, idx) => (
                      <p key={idx} style={{ margin: "0 0 8px" }}>{line || "\u00A0"}</p>
                    ))
                  ) : (
                    <span style={{ color: "#94a3b8", fontStyle: "italic" }}>
                      Your message text will appear formatted here...
                    </span>
                  )}
                </div>

                {attachedFile && (
                  <div style={{ background: "#f8fafc", border: "1px dashed #cbd5e1", borderRadius: "10px", padding: "10px 14px", marginTop: "14px", textAlign: "center" }}>
                    <p style={{ margin: 0, fontSize: "13px", fontWeight: 700, color: "#1e293b" }}>
                      <Paperclip size={14} style={{ display: "inline", verticalAlign: "middle" }} /> Attached: {attachedFile.name}
                    </p>
                  </div>
                )}
              </div>

              {/* Tips & Instructions Card */}
              <div className="panel" style={{ padding: "20px", background: "#f8fafc" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "10px" }}>
                  <Info size={18} style={{ color: "var(--primary)" }} />
                  <strong style={{ fontSize: "14px" }}>Broadcast Guidelines</strong>
                </div>
                <ul style={{ margin: 0, paddingLeft: "20px", fontSize: "13px", color: "#475569", lineHeight: 1.6 }}>
                  <li>Emails are sent instantly using the platform's SMTP / Brevo relay.</li>
                  <li>Only teams with <strong>verified payment</strong> receive this announcement.</li>
                  <li>PDF attachments are delivered directly in the inbox for participants to view or print.</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Broadcast History Table */}
          <div className="panel" style={{ padding: "24px", marginTop: "8px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "16px" }}>
              <History size={22} style={{ color: "var(--primary-dark)" }} />
              <h3 style={{ margin: 0, fontSize: "18px" }}>Broadcast History</h3>
            </div>

            {loadingHistory ? (
              <p style={{ color: "var(--muted)" }}>Loading broadcast history...</p>
            ) : history.length === 0 ? (
              <p style={{ color: "var(--muted)", fontSize: "14px" }}>No previous email broadcasts found for this tournament.</p>
            ) : (
              <div style={{ overflowX: "auto" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
                  <thead>
                    <tr style={{ borderBottom: "2px solid #e2e8f0", textAlign: "left" }}>
                      <th style={{ padding: "10px 12px", color: "#64748b" }}>Date &amp; Time</th>
                      <th style={{ padding: "10px 12px", color: "#64748b" }}>Audience / Recipients</th>
                      <th style={{ padding: "10px 12px", color: "#64748b" }}>Details &amp; Subject</th>
                      <th style={{ padding: "10px 12px", color: "#64748b" }}>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {history.map((ev) => (
                      <tr key={ev.id} style={{ borderBottom: "1px solid #f1f5f9" }}>
                        <td style={{ padding: "12px", whiteSpace: "nowrap", color: "#475569" }}>
                          {ev.created_at ? new Date(ev.created_at).toLocaleString() : "-"}
                        </td>
                        <td style={{ padding: "12px", fontWeight: 700, color: "#0f172a" }}>
                          {ev.audience}
                        </td>
                        <td style={{ padding: "12px", color: "#334155", maxWidth: "340px", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                          {ev.message}
                        </td>
                        <td style={{ padding: "12px" }}>
                          <span className={`status ${ev.status === "sent" ? "emerald" : "amber"}`}>
                            {ev.status === "sent" ? "Delivered" : ev.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </PortalShell>

      {/* Confirmation Modal */}
      {confirmModalOpen && (
        <div className="modal-backdrop">
          <section className="confirm-modal panel" style={{ maxWidth: "480px" }}>
            <div style={{ display: "grid", gap: "16px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <Send size={24} style={{ color: "var(--primary)" }} />
                <h2 style={{ margin: 0, fontSize: "20px" }}>Confirm Broadcast Email</h2>
              </div>

              <p style={{ margin: 0, color: "var(--muted)", lineHeight: 1.5, fontSize: "14px" }}>
                You are about to send an email broadcast to <strong>{recipients.length} payment-verified participants</strong> for <strong>{activeTournamentObj?.name}</strong>.
              </p>

              <div style={{ background: "#f8fafc", padding: "12px 14px", borderRadius: "10px", fontSize: "13px" }}>
                <div><strong>Subject:</strong> {subject}</div>
                {attachedFile && (
                  <div style={{ marginTop: "4px" }}><strong>Attachment:</strong> {attachedFile.name}</div>
                )}
              </div>

              <div className="registration-actions compact-actions" style={{ marginTop: "10px" }}>
                <button
                  className="btn btn-primary"
                  type="button"
                  disabled={sending}
                  onClick={executeBroadcast}
                >
                  {sending ? "Broadcasting..." : `Yes, Send to ${recipients.length} Participants`}
                </button>
                <button
                  className="btn btn-secondary"
                  type="button"
                  disabled={sending}
                  onClick={() => setConfirmModalOpen(false)}
                >
                  Cancel
                </button>
              </div>
            </div>
          </section>
        </div>
      )}
    </Page>
  );
}
