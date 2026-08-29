import { AlertCircle, Check, Edit2, Mail, Phone, Plus, ShieldCheck, Sun, Trash2, User, UserPlus } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import type { FormEvent } from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import type { AuthUser } from "../auth/AuthContext";
import { Page, PortalShell } from "../components/UI";
import { managementSidebar, sidebar, userSidebar } from "../data/platform";
import { apiRequest } from "../lib/api";
import { showToast } from "../lib/toast";

type AdminAccount = {
  id: string;
  email: string;
  name: string;
  role: string;
  phone?: string;
  created_at: string;
};

export function SettingsPage() {
  const { token, user, updateUser } = useAuth();
  const location = useLocation();

  // Password change state
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [changeOpen, setChangeOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // Edit My Profile state
  const [profileModalOpen, setProfileModalOpen] = useState(false);
  const [profileName, setProfileName] = useState(user?.name ?? "");
  const [profileEmail, setProfileEmail] = useState(user?.email ?? "");
  const [profilePhone, setProfilePhone] = useState("");
  const [profileLoading, setProfileLoading] = useState(false);

  // Super Admin Accounts Management state
  const [admins, setAdmins] = useState<AdminAccount[]>([]);
  const [adminsLoading, setAdminsLoading] = useState(false);
  const [addAdminModalOpen, setAddAdminModalOpen] = useState(false);
  const [editAdminModalOpen, setEditAdminModalOpen] = useState(false);
  const [deleteAdminModalOpen, setDeleteAdminModalOpen] = useState(false);
  const [selectedAdmin, setSelectedAdmin] = useState<AdminAccount | null>(null);

  // Add Admin form fields
  const [newAdminName, setNewAdminName] = useState("");
  const [newAdminEmail, setNewAdminEmail] = useState("");
  const [newAdminPhone, setNewAdminPhone] = useState("");
  const [newAdminPassword, setNewAdminPassword] = useState("");

  // Edit Admin form fields
  const [editAdminName, setEditAdminName] = useState("");
  const [editAdminEmail, setEditAdminEmail] = useState("");
  const [editAdminPhone, setEditAdminPhone] = useState("");
  const [editAdminPassword, setEditAdminPassword] = useState("");

  // Load Super Admin Accounts if user is super_admin
  const loadAdmins = useCallback(async () => {
    if (user?.role !== "super_admin" || !token) return;
    setAdminsLoading(true);
    try {
      const data = await apiRequest<AdminAccount[]>("/admin/admins", {}, token);
      if (Array.isArray(data)) {
        setAdmins(data);
      }
    } catch {
      // Ignore initial load error
    } finally {
      setAdminsLoading(false);
    }
  }, [user?.role, token]);

  useEffect(() => {
    loadAdmins();
  }, [loadAdmins]);

  useEffect(() => {
    if (user) {
      setProfileName(user.name ?? "");
      setProfileEmail(user.email ?? "");
    }
  }, [user]);

  // Open Edit Profile modal
  function openEditProfile() {
    setProfileName(user?.name ?? "");
    setProfileEmail(user?.email ?? "");
    setProfilePhone("");
    setProfileModalOpen(true);
  }

  // Submit Profile update
  async function submitEditProfile(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setMessage("");
    if (!profileEmail.trim() || !profileName.trim()) {
      setError("Name and Email are required.");
      return;
    }
    setProfileLoading(true);
    try {
      const updated = await apiRequest<AuthUser>("/auth/profile", {
        method: "PATCH",
        body: JSON.stringify({
          name: profileName.trim(),
          email: profileEmail.trim(),
          phone: profilePhone.trim(),
        }),
      }, token);
      updateUser(updated);
      setProfileModalOpen(false);
      setMessage("Profile and email updated successfully.");
      showToast("success", "Profile Updated", "Your profile details have been saved.");
      loadAdmins();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Failed to update profile.");
      showToast("error", "Update Failed", caught instanceof Error ? caught.message : "Failed to update profile.");
    } finally {
      setProfileLoading(false);
    }
  }

  // Open Add Admin modal
  function openAddAdmin() {
    setNewAdminName("");
    setNewAdminEmail("");
    setNewAdminPhone("");
    setNewAdminPassword("");
    setAddAdminModalOpen(true);
  }

  // Submit Add Admin
  async function submitAddAdmin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setMessage("");
    if (!newAdminName.trim() || !newAdminEmail.trim() || !newAdminPassword) {
      setError("Name, Email, and Password are required to add a Super Admin.");
      return;
    }
    try {
      await apiRequest("/admin/admins", {
        method: "POST",
        body: JSON.stringify({
          name: newAdminName.trim(),
          email: newAdminEmail.trim(),
          phone: newAdminPhone.trim(),
          password: newAdminPassword,
        }),
      }, token);
      setAddAdminModalOpen(false);
      setMessage(`Super Admin ${newAdminEmail} added successfully.`);
      showToast("success", "Admin Added", `Super Admin ${newAdminEmail} created successfully.`);
      loadAdmins();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Failed to create Super Admin.");
      showToast("error", "Creation Failed", caught instanceof Error ? caught.message : "Failed to create Super Admin.");
    }
  }

  // Open Edit Admin modal
  function openEditAdmin(admin: AdminAccount) {
    setSelectedAdmin(admin);
    setEditAdminName(admin.name);
    setEditAdminEmail(admin.email);
    setEditAdminPhone(admin.phone ?? "");
    setEditAdminPassword("");
    setEditAdminModalOpen(true);
  }

  // Submit Edit Admin
  async function submitEditAdmin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!selectedAdmin) return;
    setError("");
    setMessage("");
    if (!editAdminName.trim() || !editAdminEmail.trim()) {
      setError("Name and Email are required.");
      return;
    }
    try {
      const payload: { name: string; email: string; phone: string; password?: string } = {
        name: editAdminName.trim(),
        email: editAdminEmail.trim(),
        phone: editAdminPhone.trim(),
      };
      if (editAdminPassword.trim()) {
        payload.password = editAdminPassword.trim();
      }
      await apiRequest(`/admin/admins/${selectedAdmin.id}`, {
        method: "PATCH",
        body: JSON.stringify(payload),
      }, token);

      // If updating the currently logged in admin, also update local session
      if (selectedAdmin.id === user?.id) {
        updateUser({
          ...user,
          name: editAdminName.trim(),
          email: editAdminEmail.trim(),
        });
      }

      setEditAdminModalOpen(false);
      setMessage(`Super Admin ${editAdminEmail} updated successfully.`);
      showToast("success", "Admin Updated", `Super Admin ${editAdminEmail} updated.`);
      loadAdmins();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Failed to update Super Admin.");
      showToast("error", "Update Failed", caught instanceof Error ? caught.message : "Failed to update Super Admin.");
    }
  }

  // Open Delete Admin modal
  function openDeleteAdmin(admin: AdminAccount) {
    setSelectedAdmin(admin);
    setDeleteAdminModalOpen(true);
  }

  // Submit Delete Admin
  async function submitDeleteAdmin() {
    if (!selectedAdmin) return;
    setError("");
    setMessage("");
    try {
      await apiRequest(`/admin/admins/${selectedAdmin.id}`, {
        method: "DELETE",
      }, token);
      setDeleteAdminModalOpen(false);
      setMessage(`Super Admin ${selectedAdmin.email} deleted.`);
      showToast("success", "Admin Removed", `Super Admin ${selectedAdmin.email} was removed.`);
      loadAdmins();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Failed to delete Super Admin.");
      showToast("error", "Delete Failed", caught instanceof Error ? caught.message : "Failed to delete Super Admin.");
    }
  }

  // Password verification & change
  async function openChangePassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    setError("");
    if (!currentPassword) {
      setError("Enter your current password first.");
      showToast("warning", "Current Password Required", "Enter your current password first.");
      return;
    }
    try {
      await apiRequest("/auth/verify-password", {
        method: "POST",
        body: JSON.stringify({ current_password: currentPassword }),
      }, token);
      setChangeOpen(true);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Current password is incorrect.");
    }
  }

  async function submitChangePassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    setError("");
    if (newPassword !== confirmPassword) {
      setError("New password and confirm password must match.");
      showToast("warning", "Password Mismatch", "New password and confirm password must match.");
      return;
    }
    try {
      await apiRequest("/auth/change-password", {
        method: "POST",
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
          confirm_password: confirmPassword,
        }),
      }, token);
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
      setChangeOpen(false);
      setMessage("Password changed successfully.");
      showToast("success", "Password Changed", "Your password was updated successfully.");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Could not change password.");
    }
  }

  const portalSidebar = location.pathname.startsWith("/admin")
    ? sidebar
    : location.pathname.startsWith("/management")
      ? managementSidebar
      : userSidebar;
  const dashboardPath = user?.role === "super_admin"
    ? "/admin/dashboard"
    : user?.role === "management"
      ? "/management/dashboard"
      : "/user/dashboard";

  return (
    <Page>
      <PortalShell
        title="Profile & System Settings"
        subtitle="Manage administrator emails, account credentials, and platform appearance."
        sidebar={portalSidebar}
        action={<Link className="btn btn-primary" to={dashboardPath}>Dashboard</Link>}
      >
        {message && <div className="form-alert success-alert"><Check size={18} /> {message}</div>}
        {error && <div className="form-alert"><AlertCircle size={18} /> {error}</div>}

        {/* Panel 1: My Profile & Email */}
        <div className="panel settings-panel">
          <div className="settings-section-header">
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <User size={24} style={{ color: "var(--primary-dark)" }} />
              <h2>My Profile & Email</h2>
            </div>
            <button className="btn btn-secondary" type="button" onClick={openEditProfile}>
              <Edit2 size={14} /> Edit Profile & Email
            </button>
          </div>
          <p>Your personal account details used for system access and 2FA login verification.</p>
          
          <div className="profile-info-grid">
            <div className="profile-info-card">
              <small>Full Name</small>
              <strong>{user?.name || "Administrator"}</strong>
            </div>
            <div className="profile-info-card">
              <small>Email Address (Login & OTP)</small>
              <strong>{user?.email || "No email set"}</strong>
            </div>
            <div className="profile-info-card">
              <small>Assigned Role</small>
              <strong style={{ color: "var(--primary-dark)" }}>{user?.roleLabel || user?.role}</strong>
            </div>
          </div>
        </div>

        {/* Panel 2: Super Admin Accounts Management (Visible for Super Admin) */}
        {user?.role === "super_admin" && (
          <div className="panel settings-panel">
            <div className="settings-section-header">
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <ShieldCheck size={24} style={{ color: "var(--primary-dark)" }} />
                <h2>Super Admin Accounts</h2>
              </div>
              <button className="btn btn-primary" type="button" onClick={openAddAdmin}>
                <UserPlus size={14} /> Add Super Admin
              </button>
            </div>
            <p>Manage all administrators who have full system privileges and receive admin login OTPs.</p>

            {adminsLoading ? (
              <p style={{ color: "var(--muted)", margin: "16px 0" }}>Loading administrator accounts...</p>
            ) : (
              <div className="admin-accounts-list">
                {admins.map((adm) => {
                  const isCurrent = adm.id === user?.id || adm.email.toLowerCase() === user?.email.toLowerCase();
                  const initials = adm.name ? adm.name.slice(0, 2).toUpperCase() : "AD";
                  return (
                    <div key={adm.id} className="admin-account-item">
                      <div className="admin-account-meta">
                        <div className="admin-avatar-circle">{initials}</div>
                        <div className="admin-account-details">
                          <div className="admin-account-name-row">
                            <span className="admin-account-name">{adm.name}</span>
                            {isCurrent && <span className="admin-badge-current">You</span>}
                          </div>
                          <span className="admin-account-email">{adm.email}</span>
                        </div>
                      </div>
                      <div className="admin-account-actions">
                        <button type="button" onClick={() => openEditAdmin(adm)} title="Edit Admin">
                          <Edit2 size={13} /> Edit
                        </button>
                        {!isCurrent && admins.length > 1 && (
                          <button
                            type="button"
                            className="btn-danger-soft"
                            onClick={() => openDeleteAdmin(adm)}
                            title="Remove Admin"
                          >
                            <Trash2 size={13} /> Delete
                          </button>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* Panel 3: Change Password */}
        <form className="panel settings-panel" onSubmit={openChangePassword}>
          <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "8px" }}>
            <ShieldCheck size={24} style={{ color: "var(--primary-dark)" }} />
            <h2 style={{ margin: 0 }}>Change Password</h2>
          </div>
          <p>{user?.email ? `Signed in as ${user.email}.` : "Update your account password."}</p>
          <label>Current password
            <input type="password" placeholder="Enter current password" value={currentPassword} onChange={(event) => setCurrentPassword(event.target.value)} />
          </label>
          <button className="btn btn-primary" type="submit" style={{ marginTop: "10px" }}>Continue</button>
        </form>

        {/* Panel 4: Appearance */}
        <div className="panel settings-panel">
          <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "8px" }}>
            <Sun size={24} style={{ color: "var(--primary-dark)" }} />
            <h2 style={{ margin: 0 }}>Appearance</h2>
          </div>
          <p>Theme is fixed to the clean Smart Sportz light mode, even when the device is using dark mode.</p>
          <div className="theme-choice-grid light-only-theme" role="group" aria-label="Theme mode">
            <button className="active" type="button">
              <Sun size={18} />
              <span>Light mode</span>
              <small>Default and only active appearance for the platform.</small>
            </button>
          </div>
        </div>
      </PortalShell>

      {/* Modal: Edit My Profile & Email */}
      {profileModalOpen && (
        <div className="modal-backdrop">
          <section className="confirm-modal panel" style={{ maxWidth: "480px" }}>
            <form className="settings-password-modal" onSubmit={submitEditProfile}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <Edit2 size={22} style={{ color: "var(--primary-dark)" }} />
                <h2 style={{ margin: 0 }}>Update My Profile & Email</h2>
              </div>
              <label>Full Name
                <input
                  type="text"
                  required
                  placeholder="Administrator Name"
                  value={profileName}
                  onChange={(e) => setProfileName(e.target.value)}
                />
              </label>
              <label>Email Address
                <input
                  type="email"
                  required
                  placeholder="admin@example.com"
                  value={profileEmail}
                  onChange={(e) => setProfileEmail(e.target.value)}
                />
              </label>
              <label>Phone Number (Optional)
                <input
                  type="tel"
                  placeholder="10-digit phone number"
                  value={profilePhone}
                  onChange={(e) => setProfilePhone(e.target.value)}
                />
              </label>
              <div className="registration-actions compact-actions" style={{ marginTop: "12px" }}>
                <button className="btn btn-primary" type="submit" disabled={profileLoading}>
                  {profileLoading ? "Saving..." : "Save Changes"}
                </button>
                <button className="btn btn-secondary" type="button" onClick={() => setProfileModalOpen(false)}>
                  Cancel
                </button>
              </div>
            </form>
          </section>
        </div>
      )}

      {/* Modal: Add Super Admin */}
      {addAdminModalOpen && (
        <div className="modal-backdrop">
          <section className="confirm-modal panel" style={{ maxWidth: "480px" }}>
            <form className="settings-password-modal" onSubmit={submitAddAdmin}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <UserPlus size={22} style={{ color: "var(--primary-dark)" }} />
                <h2 style={{ margin: 0 }}>Add New Super Admin</h2>
              </div>
              <p style={{ fontSize: "13px", color: "var(--muted)", margin: 0 }}>
                This user will have full access to all settings, tournaments, payments, and logs.
              </p>
              <label>Administrator Name
                <input
                  type="text"
                  required
                  placeholder="e.g. John Doe"
                  value={newAdminName}
                  onChange={(e) => setNewAdminName(e.target.value)}
                />
              </label>
              <label>Email Address
                <input
                  type="email"
                  required
                  placeholder="admin@example.com"
                  value={newAdminEmail}
                  onChange={(e) => setNewAdminEmail(e.target.value)}
                />
              </label>
              <label>Initial Password
                <input
                  type="password"
                  required
                  placeholder="Secure password"
                  value={newAdminPassword}
                  onChange={(e) => setNewAdminPassword(e.target.value)}
                />
              </label>
              <label>Phone Number (Optional)
                <input
                  type="tel"
                  placeholder="10-digit phone number"
                  value={newAdminPhone}
                  onChange={(e) => setNewAdminPhone(e.target.value)}
                />
              </label>
              <div className="registration-actions compact-actions" style={{ marginTop: "12px" }}>
                <button className="btn btn-primary" type="submit">
                  <Plus size={16} /> Create Super Admin
                </button>
                <button className="btn btn-secondary" type="button" onClick={() => setAddAdminModalOpen(false)}>
                  Cancel
                </button>
              </div>
            </form>
          </section>
        </div>
      )}

      {/* Modal: Edit Super Admin */}
      {editAdminModalOpen && selectedAdmin && (
        <div className="modal-backdrop">
          <section className="confirm-modal panel" style={{ maxWidth: "480px" }}>
            <form className="settings-password-modal" onSubmit={submitEditAdmin}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <Edit2 size={22} style={{ color: "var(--primary-dark)" }} />
                <h2 style={{ margin: 0 }}>Edit Super Admin</h2>
              </div>
              <label>Administrator Name
                <input
                  type="text"
                  required
                  placeholder="Administrator Name"
                  value={editAdminName}
                  onChange={(e) => setEditAdminName(e.target.value)}
                />
              </label>
              <label>Email Address
                <input
                  type="email"
                  required
                  placeholder="admin@example.com"
                  value={editAdminEmail}
                  onChange={(e) => setEditAdminEmail(e.target.value)}
                />
              </label>
              <label>New Password (leave blank to keep current)
                <input
                  type="password"
                  placeholder="Leave blank to keep current password"
                  value={editAdminPassword}
                  onChange={(e) => setEditAdminPassword(e.target.value)}
                />
              </label>
              <label>Phone Number (Optional)
                <input
                  type="tel"
                  placeholder="10-digit phone number"
                  value={editAdminPhone}
                  onChange={(e) => setEditAdminPhone(e.target.value)}
                />
              </label>
              <div className="registration-actions compact-actions" style={{ marginTop: "12px" }}>
                <button className="btn btn-primary" type="submit">Save Changes</button>
                <button className="btn btn-secondary" type="button" onClick={() => setEditAdminModalOpen(false)}>
                  Cancel
                </button>
              </div>
            </form>
          </section>
        </div>
      )}

      {/* Modal: Delete Super Admin Confirmation */}
      {deleteAdminModalOpen && selectedAdmin && (
        <div className="modal-backdrop">
          <section className="confirm-modal panel" style={{ maxWidth: "440px" }}>
            <div style={{ display: "grid", gap: "14px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <Trash2 size={24} style={{ color: "#e11d48" }} />
                <h2 style={{ margin: 0 }}>Remove Super Admin</h2>
              </div>
              <p style={{ margin: 0, color: "var(--muted)", lineHeight: 1.5 }}>
                Are you sure you want to remove <strong>{selectedAdmin.name}</strong> ({selectedAdmin.email}) from Super Admin privileges?
              </p>
              <div className="registration-actions compact-actions" style={{ marginTop: "8px" }}>
                <button
                  className="btn btn-primary"
                  style={{ background: "#e11d48", borderColor: "#be123c" }}
                  type="button"
                  onClick={submitDeleteAdmin}
                >
                  Yes, Remove Admin
                </button>
                <button className="btn btn-secondary" type="button" onClick={() => setDeleteAdminModalOpen(false)}>
                  Cancel
                </button>
              </div>
            </div>
          </section>
        </div>
      )}

      {/* Modal: Password change confirmation */}
      {changeOpen && (
        <div className="modal-backdrop">
          <section className="confirm-modal panel">
            <form className="settings-password-modal" onSubmit={submitChangePassword}>
              <h2>New password</h2>
              <label>New password<input type="password" value={newPassword} onChange={(event) => setNewPassword(event.target.value)} /></label>
              <label>Confirm password<input type="password" value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)} /></label>
              <div className="registration-actions compact-actions">
                <button className="btn btn-primary" type="submit">Change Password</button>
                <button className="btn btn-secondary" type="button" onClick={() => setChangeOpen(false)}>Cancel</button>
              </div>
            </form>
          </section>
        </div>
      )}
    </Page>
  );
}

