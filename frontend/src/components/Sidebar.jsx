import {
  FaChartLine,
  FaCreditCard,
  FaBell,
  FaBrain,
  FaUpload,
  FaSignOutAlt,
  FaShieldAlt
} from "react-icons/fa";

import {
  NavLink,
  useNavigate
} from "react-router-dom";

function Sidebar() {

  const navigate = useNavigate();

  const handleLogout = () => {

    localStorage.removeItem("token");

    navigate("/");
  };

  const menuClass = ({ isActive }) =>
    `flex items-center gap-3 p-3 rounded-lg transition-all duration-200 ${
      isActive
        ? "bg-blue-600 text-white"
        : "hover:bg-gray-800"
    }`;

  return (

    <div className="fixed left-0 top-0 w-64 h-screen bg-gray-900 text-white shadow-xl">

      <div className="p-6">

        <div className="flex items-center gap-3 mb-10">

          <FaShieldAlt size={30} />

          <h1 className="text-2xl font-bold">
            Fraud Admin
          </h1>

        </div>

        <nav className="flex flex-col gap-3">

          <NavLink
            to="/dashboard"
            className={menuClass}
          >
            <FaChartLine />
            Dashboard
          </NavLink>

          <NavLink
            to="/upload"
            className={menuClass}
          >
            <FaUpload />
            Upload Transactions
          </NavLink>

          <NavLink
            to="/transactions"
            className={menuClass}
          >
            <FaCreditCard />
            Transactions
          </NavLink>

          <NavLink
            to="/alerts"
            className={menuClass}
          >
            <FaBell />
            Alerts
          </NavLink>

          <NavLink
            to="/predictions"
            className={menuClass}
          >
            <FaBrain />
            Predictions
          </NavLink>

          <button
            onClick={handleLogout}
            className="flex items-center gap-3 mt-10 p-3 rounded-lg hover:bg-red-600 transition-all"
          >
            <FaSignOutAlt />
            Logout
          </button>

        </nav>

      </div>

    </div>
  );
}

export default Sidebar;