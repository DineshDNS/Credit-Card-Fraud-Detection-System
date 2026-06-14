import { Link, useNavigate } from "react-router-dom";

function Sidebar() {

  const navigate = useNavigate();

  const handleLogout = () => {

    localStorage.removeItem("token");

    navigate("/");
  };

  return (
    <div className="w-64 min-h-screen bg-gray-900 text-white p-6">

      <h1 className="text-2xl font-bold mb-10">
        Fraud Admin
      </h1>

      <nav className="flex flex-col gap-4">

        <Link
          to="/dashboard"
          className="hover:bg-gray-700 p-3 rounded"
        >
          📊 Dashboard
        </Link>

        <Link
          to="/transactions"
          className="hover:bg-gray-700 p-3 rounded"
        >
          💳 Transactions
        </Link>

        <Link
          to="/alerts"
          className="hover:bg-gray-700 p-3 rounded"
        >
          🚨 Alerts
        </Link>

        <Link
          to="/predictions"
          className="hover:bg-gray-700 p-3 rounded"
        >
          🤖 Predictions
        </Link>

        <Link
            to="/simulator"
            className="flex items-center gap-3"
            >
            🧠 Simulator
            </Link>

        <button
          onClick={handleLogout}
          className="text-left hover:bg-red-700 p-3 rounded mt-8"
        >
          🚪 Logout
        </button>

      </nav>

    </div>
  );
}

export default Sidebar;