import { Navigate } from "react-router-dom";

export function Protect ({ isLoggedIn, children }) {
  console.log('protect ', isLoggedIn)
  if (!isLoggedIn) {
    return <Navigate to="/home  " replace />;
  }
  return children;
};
