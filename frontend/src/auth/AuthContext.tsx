import {
  createContext,
  useContext,
  useState,
  type ReactNode,
} from "react";
 
import { loginRequest } from "../api/auth.api";
 
import type {
  AuthUser,
  LoginPayload,
} from "../types/auth";
 
 
interface AuthContextType {
  user: AuthUser | null;
  token: string | null;
  isAuthenticated: boolean;
 
  login: (
    payload: LoginPayload
  ) => Promise<void>;
 
  logout: () => void;
 
  hasPermission: (
    permission: string
  ) => boolean;
}
 
 
const AuthContext = createContext<
  AuthContextType | undefined
>(undefined);
 
 
function loadStoredUser(): AuthUser | null {
  const stored = localStorage.getItem(
    "current_user"
  );
 
  if (!stored) {
    return null;
  }
 
  try {
    return JSON.parse(stored);
  } catch {
    localStorage.removeItem(
      "current_user"
    );
 
    return null;
  }
}
 
 
export function AuthProvider({
  children,
}: {
  children: ReactNode;
}) {
 
  const [token, setToken] = useState<
    string | null
  >(
    localStorage.getItem(
      "access_token"
    )
  );
 
  const [user, setUser] = useState<
    AuthUser | null
  >(
    loadStoredUser()
  );
 
 
  async function login(
    payload: LoginPayload
  ) {
 
    const result = await loginRequest(
      payload
    );
 
    localStorage.setItem(
      "access_token",
      result.access_token
    );
 
    setToken(
      result.access_token
    );
 
    if (result.user) {
      localStorage.setItem(
        "current_user",
        JSON.stringify(
          result.user
        )
      );
 
      setUser(
        result.user
      );
    }
  }
 
 
  function logout() {
 
    localStorage.removeItem(
      "access_token"
    );
 
    localStorage.removeItem(
      "current_user"
    );
 
    setToken(null);
    setUser(null);
  }
 
 
  function hasPermission(
    permission: string
  ) {
 
    if (!user?.permissions) {
      return false;
    }
 
    return (
      user.permissions.includes("*")
      ||
      user.permissions.includes(
        permission
      )
    );
  }
 
 
  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: Boolean(
          token
        ),
        login,
        logout,
        hasPermission,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
 
 
export function useAuth() {
 
  const context = useContext(
    AuthContext
  );
 
  if (!context) {
    throw new Error(
      "useAuth must be used inside AuthProvider"
    );
  }
 
  return context;
}