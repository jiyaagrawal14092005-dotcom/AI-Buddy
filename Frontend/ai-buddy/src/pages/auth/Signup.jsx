import { useState } from "react";
import {
    Eye,
    EyeOff,
    ArrowRight,
    Sparkles,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

function Signup() {
    const navigate = useNavigate();

    const [showPassword, setShowPassword] = useState(false);
    const [showConfirm, setShowConfirm] = useState(false);

    const [fullName, setFullName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");

    const handleSignup = (e) => {
        e.preventDefault();

        if (!fullName.trim()) {
            setError("Please enter your full name.");
            return;
        }

        if (!email.trim()) {
            setError("Please enter your email.");
            return;
        }

        if (!email.includes("@")) {
            setError("Please enter a valid email.");
            return;
        }

        if (!password.trim()) {
            setError("Please enter your password.");
            return;
        }

        if (password.length < 6) {
            setError("Password must be at least 6 characters.");
            return;
        }

        if (!confirmPassword.trim()) {
            setError("Please confirm your password.");
            return;
        }

        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        setError("");

        // Backend signup will be connected later.
        console.log("Signup:", {
            fullName,
            email,
            password,
        });
    };

    return (
        <div className="zarvis-signup-page">

            <div className="zarvis-signup-bg-glow"></div>
            <div className="zarvis-signup-stars"></div>

            <div className="zarvis-signup-container">

                {/* LEFT */}
                <section className="zarvis-signup-left">

                    <div className="zarvis-signup-brand">

                        <div className="zarvis-signup-brand-icon">
                            <Sparkles size={19} />
                        </div>

                        <span>ZARVIS</span>

                    </div>

                    <h1>
                        Your AI Buddy.
                        <br />
                        <span>Always With You.</span>
                    </h1>

                    <p>
                        Plan&nbsp; • &nbsp;Learn&nbsp; • &nbsp;Work&nbsp; • &nbsp;Grow
                    </p>

                    <div className="zarvis-signup-message">
                        ✦ Great things start with you
                    </div>

                </section>

                {/* RIGHT */}
                <section className="zarvis-signup-card">

                    <div className="zarvis-signup-card-brand">

                        <Sparkles size={17} />

                        <span>ZARVIS</span>

                    </div>

                    <h2>Create your account</h2>

                    <p className="zarvis-signup-subtitle">
                        Start your journey with your AI buddy.
                    </p>

                    <form
                        className="zarvis-signup-form"
                        onSubmit={handleSignup}
                    >

                        {/* NAME */}
                        <div className="zarvis-signup-field">

                            <label>Full Name</label>

                            <input
                                type="text"
                                placeholder="Enter your name"
                                value={fullName}
                                onChange={(e) => {
                                    setFullName(e.target.value);
                                    setError("");
                                }}
                            />

                        </div>

                        {/* EMAIL */}
                        <div className="zarvis-signup-field">

                            <label>Email</label>

                            <input
                                type="email"
                                placeholder="Enter your email"
                                value={email}
                                onChange={(e) => {
                                    setEmail(e.target.value);
                                    setError("");
                                }}
                            />

                        </div>

                        {/* PASSWORD */}
                        <div className="zarvis-signup-field">

                            <label>Password</label>

                            <div className="zarvis-signup-password">

                                <input
                                    type={
                                        showPassword
                                            ? "text"
                                            : "password"
                                    }
                                    placeholder="Create password"
                                    value={password}
                                    onChange={(e) => {
                                        setPassword(e.target.value);
                                        setError("");
                                    }}
                                />

                                <button
                                    type="button"
                                    onClick={() =>
                                        setShowPassword(
                                            !showPassword
                                        )
                                    }
                                >
                                    {showPassword ? (
                                        <EyeOff size={17} />
                                    ) : (
                                        <Eye size={17} />
                                    )}
                                </button>

                            </div>

                        </div>

                        {/* CONFIRM PASSWORD */}
                        <div className="zarvis-signup-field">

                            <label>Confirm Password</label>

                            <div className="zarvis-signup-password">

                                <input
                                    type={
                                        showConfirm
                                            ? "text"
                                            : "password"
                                    }
                                    placeholder="Confirm password"
                                    value={confirmPassword}
                                    onChange={(e) => {
                                        setConfirmPassword(
                                            e.target.value
                                        );
                                        setError("");
                                    }}
                                />

                                <button
                                    type="button"
                                    onClick={() =>
                                        setShowConfirm(
                                            !showConfirm
                                        )
                                    }
                                >
                                    {showConfirm ? (
                                        <EyeOff size={17} />
                                    ) : (
                                        <Eye size={17} />
                                    )}
                                </button>

                            </div>

                        </div>

                        {/* ERROR */}
                        {error && (
                            <div
                                style={{
                                    color: "#f0a4ff",
                                    fontSize: "12px",
                                    textAlign: "center",
                                    marginTop: "-4px",
                                }}
                            >
                                {error}
                            </div>
                        )}

                        {/* CREATE ACCOUNT */}
                        <button
                            type="submit"
                            className="zarvis-signup-submit"
                        >
                            <span>Create Account</span>

                            <ArrowRight size={17} />
                        </button>

                    </form>

                    {/* LOGIN */}
                    <div className="zarvis-signup-login">

                        <span>
                            Already have an account?
                        </span>

                        <button
                            type="button"
                            onClick={() => navigate("/login")}
                        >
                            Login

                            <ArrowRight size={14} />
                        </button>

                    </div>

                </section>

            </div>

        </div>
    );
}

export default Signup;