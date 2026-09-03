import { useState, type FormEvent } from "react";
import { motion } from "framer-motion";
import { Page } from "../components/UI";
import { apiRequest } from "../lib/api";
import {
  Mail,
  Phone,
  MapPin,
  Clock,
  Send,
  CheckCircle2,
  AlertCircle,
  MessageSquare,
  Sparkles,
  ExternalLink
} from "lucide-react";

export function ContactPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [subject, setSubject] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const adminEmail = "python.asmath1290@gmail.com";
  const supportEmail = "info@smartsportz.in";
  const primaryPhone = "+91 78713 57999";
  const secondaryPhone = "+91 63744 09006";

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setErrorMessage(null);
    setSuccessMessage(null);

    if (!name.trim() || !email.trim() || !subject.trim() || !message.trim()) {
      setErrorMessage("Please complete all required fields (Name, Email, Subject, and Message).");
      return;
    }

    setLoading(true);
    try {
      const result = await apiRequest<{ message: string }>("/public/contact", {
        method: "POST",
        body: JSON.stringify({
          name: name.trim(),
          email: email.trim(),
          phone: phone.trim(),
          subject: subject.trim(),
          message: message.trim(),
        }),
      });

      setSuccessMessage(
        result?.message ||
          `Thank you! Your message has been sent to the admin email (${adminEmail}). We will get back to you shortly.`
      );
      setName("");
      setEmail("");
      setPhone("");
      setSubject("");
      setMessage("");
    } catch (err: any) {
      const detail =
        err?.response?.data?.detail ||
        err?.message ||
        "Could not send email right now. You can also email the admin directly at " + adminEmail;
      setErrorMessage(typeof detail === "string" ? detail : "Failed to deliver inquiry.");
    } finally {
      setLoading(false);
    }
  }

  const fadeInUp = {
    hidden: { opacity: 0, y: 24 },
    visible: (customDelay: number = 0) => ({
      opacity: 1,
      y: 0,
      transition: { duration: 0.55, delay: customDelay, ease: [0.22, 1, 0.36, 1] },
    }),
  };

  return (
    <Page className="contact-page-wrapper">
      <div className="contact-container">
        {/* Header Hero */}
        <section className="contact-hero">
          <motion.div
            initial="hidden"
            animate="visible"
            variants={{ visible: { transition: { staggerChildren: 0.1 } } }}
          >
            <motion.div variants={fadeInUp} custom={0} className="contact-eyebrow-pill">
              <Sparkles size={14} />
              <span>GET IN TOUCH</span>
            </motion.div>
            <motion.h1 variants={fadeInUp} custom={0.1} className="contact-title">
              Contact SmartSportz
            </motion.h1>
            <motion.p variants={fadeInUp} custom={0.2} className="contact-subtitle">
              Reach out to our tournament directors and administrative team. Send an inquiry directly to the administrator's email or contact us through our official phone lines.
            </motion.p>
          </motion.div>
        </section>

        {/* Main Grid: Details + Form */}
        <div className="contact-layout-grid">
          {/* Left Column: Admin Contact Details */}
          <motion.div
            className="contact-info-column"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            variants={{ visible: { transition: { staggerChildren: 0.12 } } }}
          >
            <motion.div variants={fadeInUp} className="contact-details-intro">
              <h2>Admin Contact Information</h2>
              <p>
                Have questions about tournament registrations, sponsorship opportunities, fixtures, or technical support? Contact the SmartSportz administration directly.
              </p>
            </motion.div>

            {/* Email Card */}
            <motion.div variants={fadeInUp} className="contact-detail-card">
              <div className="contact-card-icon-wrap email">
                <Mail size={22} />
              </div>
              <div className="contact-card-content">
                <span className="contact-card-label">Admin Email Address</span>
                <a href={`mailto:${adminEmail}`} className="contact-card-primary-link">
                  {adminEmail}
                </a>
                <div className="contact-card-sub-info">
                  <span>General Support: </span>
                  <a href={`mailto:${supportEmail}`}>{supportEmail}</a>
                </div>
              </div>
            </motion.div>

            {/* Phone & WhatsApp Card */}
            <motion.div variants={fadeInUp} className="contact-detail-card">
              <div className="contact-card-icon-wrap phone">
                <Phone size={22} />
              </div>
              <div className="contact-card-content">
                <span className="contact-card-label">Phone & WhatsApp Support</span>
                <div className="contact-card-links-row">
                  <a href={`tel:${primaryPhone.replace(/\s+/g, "")}`} className="contact-card-primary-link">
                    {primaryPhone}
                  </a>
                  <span className="contact-badge-pill">Primary</span>
                </div>
                <div className="contact-card-sub-info">
                  <span>Helpline: </span>
                  <a href={`tel:${secondaryPhone.replace(/\s+/g, "")}`}>{secondaryPhone}</a>
                </div>
                <a
                  href={`https://wa.me/917871357999?text=${encodeURIComponent("Hello SmartSportz Admin, I would like to inquire about tournaments.")}`}
                  target="_blank"
                  rel="noreferrer"
                  className="contact-whatsapp-link"
                >
                  <MessageSquare size={14} />
                  <span>Chat on WhatsApp</span>
                  <ExternalLink size={12} />
                </a>
              </div>
            </motion.div>

            {/* Location Card */}
            <motion.div variants={fadeInUp} className="contact-detail-card">
              <div className="contact-card-icon-wrap location">
                <MapPin size={22} />
              </div>
              <div className="contact-card-content">
                <span className="contact-card-label">Operational Headquarters</span>
                <strong className="contact-card-heading">Bengaluru, Karnataka, India</strong>
                <p className="contact-card-text">
                  Hosting youth, collegiate, corporate, and open community sports tournaments across India.
                </p>
              </div>
            </motion.div>

            {/* Working Hours Card */}
            <motion.div variants={fadeInUp} className="contact-detail-card">
              <div className="contact-card-icon-wrap hours">
                <Clock size={22} />
              </div>
              <div className="contact-card-content">
                <span className="contact-card-label">Operating Schedule</span>
                <strong className="contact-card-heading">Monday – Saturday: 9:00 AM – 7:00 PM IST</strong>
                <p className="contact-card-text">
                  Inquiries received outside operational hours are reviewed the following morning.
                </p>
              </div>
            </motion.div>
          </motion.div>

          {/* Right Column: Email Send Form */}
          <motion.div
            className="contact-form-column"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            variants={fadeInUp}
          >
            <div className="contact-form-card">
              <div className="contact-form-header">
                <div className="contact-form-icon-pill">
                  <Send size={18} />
                  <span>SEND EMAIL TO ADMIN</span>
                </div>
                <h3>Send Inquiry Directly</h3>
                <p>
                  Submit the form below and an email notification will be dispatched straight to the administrator's mailbox (<strong>{adminEmail}</strong>).
                </p>
              </div>

              {successMessage && (
                <div className="contact-alert success">
                  <CheckCircle2 size={20} className="alert-icon" />
                  <div>
                    <strong>Message Sent Successfully!</strong>
                    <p>{successMessage}</p>
                  </div>
                </div>
              )}

              {errorMessage && (
                <div className="contact-alert error">
                  <AlertCircle size={20} className="alert-icon" />
                  <div>
                    <strong>Unable to send message</strong>
                    <p>{errorMessage}</p>
                  </div>
                </div>
              )}

              <form onSubmit={handleSubmit} className="contact-form">
                <div className="contact-form-row">
                  <div className="contact-form-group">
                    <label htmlFor="contact-name">
                      Your Full Name <span className="req">*</span>
                    </label>
                    <input
                      id="contact-name"
                      type="text"
                      placeholder="e.g. Rahul Sharma"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      required
                    />
                  </div>

                  <div className="contact-form-group">
                    <label htmlFor="contact-email">
                      Your Email Address <span className="req">*</span>
                    </label>
                    <input
                      id="contact-email"
                      type="email"
                      placeholder="e.g. rahul@example.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </div>
                </div>

                <div className="contact-form-row">
                  <div className="contact-form-group">
                    <label htmlFor="contact-phone">
                      Phone Number / WhatsApp <small>(Optional)</small>
                    </label>
                    <input
                      id="contact-phone"
                      type="tel"
                      placeholder="e.g. +91 98765 43210"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                    />
                  </div>

                  <div className="contact-form-group">
                    <label htmlFor="contact-subject">
                      Subject / Topic <span className="req">*</span>
                    </label>
                    <input
                      id="contact-subject"
                      type="text"
                      placeholder="e.g. Tournament Registration Inquiry"
                      value={subject}
                      onChange={(e) => setSubject(e.target.value)}
                      required
                    />
                  </div>
                </div>

                <div className="contact-form-group">
                  <label htmlFor="contact-message">
                    Your Message <span className="req">*</span>
                  </label>
                  <textarea
                    id="contact-message"
                    rows={5}
                    placeholder="Write your message or inquiry here. Please include any relevant tournament or team details..."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    required
                  />
                </div>

                <div className="contact-form-actions">
                  <button
                    type="submit"
                    className="contact-submit-btn"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="contact-spinner" />
                        <span>Sending to Admin...</span>
                      </>
                    ) : (
                      <>
                        <Send size={16} />
                        <span>Send Email to Admin</span>
                      </>
                    )}
                  </button>

                  <a
                    href={`mailto:${adminEmail}?subject=${encodeURIComponent(subject || "SmartSportz Inquiry")}&body=${encodeURIComponent(message || "")}`}
                    className="contact-direct-mailto-link"
                    title="Open your default email client"
                  >
                    <span>Open in Email App</span>
                    <ExternalLink size={13} />
                  </a>
                </div>
              </form>
            </div>
          </motion.div>
        </div>
      </div>
    </Page>
  );
}
