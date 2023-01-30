import { Navigate } from "react-router-dom";

export function Protect ({ isLoggedIn, children }) {
  console.log('what is props ', isLoggedIn)
  if (!isLoggedIn.isloggedInStatus) {
    return <Navigate to="/home  " replace />;
  }
  return children;
};
