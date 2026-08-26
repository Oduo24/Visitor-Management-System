import {
  NavLink,
  Outlet,
} from "react-router-dom";
 
import { useAuth } from "../../auth/AuthContext";
 
 
export function AppLayout() {
 
  const {
    user,
    logout,
  } = useAuth();
 
  const name = [
    user?.first_name,
    user?.last_name,
  ]
    .filter(Boolean)
    .join(" ");
 
 
  return (
    <div className="app-shell">
 
      <aside className="sidebar">
 
        <div className="sidebar-brand">
          VMS
        </div>
 
        <nav>
 
          <NavLink
            to="/dashboard"
          >
            Dashboard
          </NavLink>
 
          <NavLink
            to="/visits"
          >
            Visits
          </NavLink>
 
          <NavLink
            to="/visitors"
          >
            Visitors
          </NavLink>

          <NavLink
            to="/qr-kiosk"
          >
            QR Kiosk
          </NavLink>
 
        </nav>
 
      </aside>
 
 
      <div className="app-main">
 
        <header className="app-header">
 
          <div>
            {
              name
              ||
              user?.email
              ||
              "User"
            }
          </div>
 
          <button
            onClick={logout}
          >
            Logout
          </button>
 
        </header>
 
 
        <main className="page-content">
          <Outlet />
        </main>
 
      </div>
 
    </div>
  );
}