import sys

with open('frontend/src/pages/LoginPage.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<form onSubmit={handleSubmit}>')
end = text.find('</form>', start)
form_content = text[start:end+7]

new_form = '''<form onSubmit={handleSubmit}>
          {!recovery && !challenge && mode === "login" ? (
            <>
              <h1 style={{ marginBottom: "4px", textAlign: "center" }}>Welcome back</h1>
              <div style={{ textAlign: "center", marginBottom: "24px", color: "var(--muted)" }}>
                <span>Don't have an account? </span>
                <button className="auth-switch-inline" type="button" style={{ background: "none", border: "none", color: "var(--primary)", cursor: "pointer", padding: 0, font: "inherit" }} onClick={() => { setMode("signup"); setError(""); }}>Sign up.</button>
              </div>
            </>
          ) : (
            <>
              <Lock size={28} />
              <h1>{recovery ? "Forgot Password?" : mode === "signup" ? "Create Account" : "Welcome Back"}</h1>
              <p>
                {challenge
                  ? challenge.deliveryMessage || \Enter the verification code sent to \.\
                  : recovery
                    ? "Enter your email and verify the account by verification code."
                    : mode === "signup"
                      ? "Create a participant account and verify it before opening your dashboard."
                      : "Please enter your credentials to access your dashboard."}
              </p>
            </>
          )}

          {!challenge && !recovery && mode === "login" && (
            <div className="google-login-wrap" style={{ marginBottom: "16px", marginTop: "16px" }}>
              {googleClientId ? (
                <div ref={googleButtonRef} className="google-identity-button" />
              ) : (
                <button className="google-login-button" type="button" onClick={() => setError("Google login could not initialize. Refresh the page and confirm this domain is allowed in Google Cloud OAuth origins.")}>
                  <span className="google-mark" aria-hidden="true">G</span>
                  Continue with Google
                </button>
              )}
            </div>
          )}

          {!challenge && !recovery && mode === "login" && (
            <div style={{ display: "flex", alignItems: "center", textAlign: "center", margin: "24px 0", color: "var(--muted)", fontSize: "13px" }}>
              <div style={{ flex: 1, height: "1px", backgroundColor: "var(--line)" }}></div>
              <span style={{ padding: "0 10px" }}>Or continue with username/email</span>
              <div style={{ flex: 1, height: "1px", backgroundColor: "var(--line)" }}></div>
            </div>
          )}

          {!challenge && mode === "signup" && <label>Full name<input placeholder="Team captain name" value={name} onChange={(event) => setName(event.target.value)} /></label>}
          {!challenge && <label>{!recovery && mode === "login" ? "Username or email address" : "Email address"}<input placeholder={!recovery && mode === "login" ? "" : "example@gmail.com"} value={email} onChange={(event) => setEmail(event.target.value)} /></label>}
          {!challenge && mode === "signup" && <label>Phone number<input type="tel" inputMode="numeric" maxLength={10} pattern="[0-9]{10}" placeholder="10 digit phone" value={phone} onChange={(event) => setPhone(phoneDigits(event.target.value))} /></label>}
          {!challenge && !recovery && (
            <label className="password-field">
              Password
              <div className="password-input-wrap">
                <input
                  placeholder=""
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                />
                <button
                  type="button"
                  className="password-toggle"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  onClick={() => setShowPassword((current) => !current)}
                  style={{ fontSize: "14px", color: "var(--primary)", fontWeight: "600", background: "none", border: "none" }}
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </label>
          )}

          {!recovery && mode === "login" && <div style={{ textAlign: "left", marginTop: "-8px", marginBottom: "20px" }}><Link to="/forgot-password" style={{ fontSize: "13px", color: "var(--primary)", fontWeight: "500" }}>Forgot your password?</Link></div>}

          {!challenge && mode === "signup" && <div className="otp-channel-group"><button type="button" className="active">Verify by OTP</button></div>}
          {challenge && <label>Verification code<input placeholder="4 digit code" value={otp} onChange={(event) => setOtp(event.target.value)} maxLength={8} /></label>}
          {challenge && recovery && <label>New password<input placeholder="New secure password" type="password" value={newPassword} onChange={(event) => setNewPassword(event.target.value)} /></label>}
          
          {error && <div className="form-alert">{error}</div>}
          <button type="submit" className="btn btn-primary wide" disabled={loading} style={{ padding: "12px", fontSize: "15px" }}>
            {loading ? "Please wait..." : challenge ? "Verify OTP" : recovery ? "Send OTP" : mode === "signup" ? "Create and verify account" : "Sign in"}
          </button>

          {!recovery && !challenge && mode === "login" && (
            <div style={{ textAlign: "center", marginTop: "24px", color: "var(--text)" }}>
              <span>Don't have an account? </span>
              <button className="auth-switch-inline" type="button" style={{ background: "none", border: "none", color: "var(--primary)", cursor: "pointer", padding: 0, font: "inherit", fontWeight: "600" }} onClick={() => { setMode("signup"); setError(""); }}>Sign up</button>
            </div>
          )}

          {!recovery && !challenge && mode === "signup" && (
            <div style={{ textAlign: "center", marginTop: "20px", color: "var(--muted)" }}>
              <span>Already have an account? </span>
              <button className="auth-switch-inline" type="button" style={{ background: "none", border: "none", color: "var(--primary)", cursor: "pointer", padding: 0, font: "inherit", fontWeight: "600" }} onClick={() => { setMode("login"); setError(""); }}>Sign in</button>
            </div>
          )}
          
          {challenge && <button className="auth-switch" type="button" onClick={() => { setChallenge(null); setOtp(""); }}>Change details</button>}
          {recovery && <div style={{ textAlign: "center", marginTop: "20px" }}><Link to="/login">Back to login</Link></div>}
        </form>'''

text = text.replace(form_content, new_form)
with open('frontend/src/pages/LoginPage.tsx', 'w', encoding='utf-8') as f:
    f.write(text)
