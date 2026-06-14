import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await api.post(
        `/login?username=${username}&password=${password}`
      );

      localStorage.setItem(
        "token",
        response.data.access_token
      );

      navigate("/dashboard");
    } catch (error) {
      alert("Login Failed");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleLogin}
        className="w-96 rounded-lg border bg-white p-6 shadow-lg"
      >
        <h1 className="mb-6 text-center text-2xl font-bold">
          Admin Login
        </h1>

        <input
          type="text"
          placeholder="Username"
          className="mb-4 w-full rounded border p-2"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="mb-4 w-full rounded border p-2"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          type="submit"
          className="w-full rounded bg-blue-500 p-2 text-white hover:bg-blue-600"
        >
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;