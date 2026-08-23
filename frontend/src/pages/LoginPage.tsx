import {
  useState,
  type FormEvent,
} from "react";
 
import axios from "axios";
 
import {
  Navigate,
  useLocation,
  useNavigate,
} from "react-router-dom";
 
import { useAuth } from "../auth/AuthContext";
 
 
export function LoginPage() {
 
  const {
    login,
    isAuthenticated,
  } = useAuth();
 
  const navigate = useNavigate();
  const location = useLocation();
 
  const [email, setEmail] =
    useState("");
 
  const [password, setPassword] =
    useState("");
 
  const [loading, setLoading] =
    useState(false);
 
  const [error, setError] =
    useState<string | null>(
      null
    );
 
 
  if (isAuthenticated) {
    return (
      <Navigate
        to="/dashboard"
        replace
      />
    );
  }
 
 
  async function handleSubmit(
    event: FormEvent
  ) {
 
    event.preventDefault();
 
    setLoading(true);
    setError(null);
 
    try {
 
      await login({
        email,
        password,
      });
 
      const previousPath =
        (
          location.state as {
            from?: string;
          } | null
        )?.from;
 
      navigate(
        previousPath
        ?? "/dashboard",
        {
          replace: true,
        }
      );
 
    } catch (err) {
 
      if (axios.isAxiosError(err)) {
 
        const responseData =
          err.response?.data as {
            message?: string;
            error?: string;
          } | undefined;
 
        setError(
          responseData?.message
          ??
          responseData?.error
          ??
          "Unable to login."
        );
 
      } else {
        setError(
          "Unable to login."
        );
      }
 
    } finally {
      setLoading(false);
    }
  }
 
 
  return (
    <div className="login-page">
 
      <div className="login-card">
 
        <h1>
          Visitor Management
        </h1>
 
        <p>
          Sign in to continue
        </p>
 
        {error && (
          <div className="form-error">
            {error}
          </div>
        )}
 
        <form
          onSubmit={
            handleSubmit
          }
        >
 
          <label>
            Email
          </label>
 
          <input
            type="email"
            value={email}
            onChange={(event) =>
              setEmail(
                event.target.value
              )
            }
            required
            autoComplete="email"
          />
 
          <label>
            Password
          </label>
 
          <input
            type="password"
            value={password}
            onChange={(event) =>
              setPassword(
                event.target.value
              )
            }
            required
            autoComplete="current-password"
          />
 
          <button
            type="submit"
            disabled={loading}
          >
            {
              loading
              ? "Signing in..."
              : "Sign in"
            }
          </button>
 
        </form>
 
      </div>
 
    </div>
  );
}