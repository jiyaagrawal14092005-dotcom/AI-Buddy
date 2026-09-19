import { useState } from "react";
import {
    Eye,
    EyeOff,
    ArrowRight,
    Sparkles,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

function Login() {
    const navigate = useNavigate();
    const { login } = useAuth();

    const [showPassword, setShowPassword] = useState(false);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleLogin = async (e) => {
        e.preventDefault();

        if (!email.trim() || !password.trim()) {
            setError("Please enter your email and password.");
            return;
        }

        if (password.length < 6) {
            setError("Password must be at least 6 characters.");
            return;
        }

        setError("");
        setLoading(true);

        try {
            await login({
                email: email.trim(),
                password,
            });

            // Login successful
            navigate("/assistant");
        } catch (error) {
            console.error("Login failed:", error);

            setError(
                error?.message ||
                "Login failed. Please check your email and password."
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="zarvis-login-page">

            <div className="zarvis-login-bg-glow"></div>
            <div className="zarvis-login-stars"></div>

            <div className="zarvis-login-container">

                <section className="zarvis-login-left">

                    <div className="zarvis-login-brand">
                        <div className="zarvis-login-brand-icon">
                            <Sparkles size={19} />
                        </div>

                        <span>ZARVIS</span>
                    </div>

                    <h1>
                        Welcome Back.
                        <br />
                        <span>Your AI Buddy Is Here.</span>
                    </h1>

                    <p>
                        Plan&nbsp; • &nbsp;Learn&nbsp; • &nbsp;Work&nbsp; • &nbsp;Grow
                    </p>

                    <div className="zarvis-login-message">
                        ✦ Let's get things done together
                    </div>

                </section>

                <section className="zarvis-login-card">

                    <div className="zarvis-login-card-brand">
                        <Sparkles size={17} />
                        <span>ZARVIS</span>
                    </div>

                    <h2>Welcome back</h2>

                    <p className="zarvis-login-subtitle">
                        Login to continue with your AI buddy.
                    </p>

                    <form
                        className="zarvis-login-form"
                        onSubmit={handleLogin}
                    >

                        <div className="zarvis-login-field">

                            <label>Email</label>

                            <input
                                type="email"
                                placeholder="Enter your email"
                                value={email}
                                onChange={(e) => {
                                    setEmail(e.target.value);
                                    setError("");
                                }}
                                disabled={loading}
                            />

                        </div>

                        <div className="zarvis-login-field">

                            <label>Password</label>

                            <div className="zarvis-login-password">

                                <input
                                    type={
                                        showPassword
                                            ? "text"
                                            : "password"
                                    }
                                    placeholder="Enter your password"
                                    value={password}
                                    onChange={(e) => {
                                        setPassword(e.target.value);
                                        setError("");
                                    }}
                                    disabled={loading}
                                />

                                <button
                                    type="button"
                                    onClick={() =>
                                        setShowPassword(
                                            !showPassword
                                        )
                                    }
                                    disabled={loading}
                                >
                                    {showPassword ? (
                                        <EyeOff size={17} />
                                    ) : (
                                        <Eye size={17} />
                                    )}
                                </button>

                            </div>

                        </div>

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

                        <button
                            type="submit"
                            className="zarvis-login-submit"
                            disabled={loading}
                        >
                            <span>
                                {loading
                                    ? "Logging in..."
                                    : "Login"}
                            </span>

                            {!loading && (
                                <ArrowRight size={17} />
                            )}
                        </button>

                    </form>

                    <div className="zarvis-login-signup">

                        <span>
                            Don't have an account?
                        </span>

                        <button
                            type="button"
                            onClick={() => navigate("/signup")}
                            disabled={loading}
                        >
                            Sign Up
                            <ArrowRight size={14} />
                        </button>

                    </div>

                </section>

            </div>

        </div>
    );
}

export default Login;