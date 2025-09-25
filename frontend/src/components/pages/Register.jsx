import { useState } from "react";
import axios from "axios";

function Register() {
    const [form, setForm] = useState({ username: "", email: "", password: "" });

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post("http://127.0.0.1:8000/api/register/", form);
            console.log("Form data sent:", form);
            console.log("Registered! Token: " + res.data.token);
            // console.log(":", form);

            // Save token to localStorage
            localStorage.setItem("token", res.data.token);

        } catch (err) {
            // Show detailed backend error
            console.error(err.response?.data);
            alert("Registration failed: " + JSON.stringify(err.response?.data));
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                name="username"
                placeholder="Username"
                value={form.username}
                onChange={handleChange}
                required
            />
            <input
                type="email"
                name="email"
                placeholder="Email"
                value={form.email}
                onChange={handleChange}
            />
            <input
                type="password"
                name="password"
                placeholder="Password"
                value={form.password}
                onChange={handleChange}
                required
            />
            <button type="submit">Register</button>
        </form>
    );
}

export default Register;
