import React from 'react';
 import { useState } from 'react';
 import axios from 'axios';
 import { useNavigate } from 'react-router-dom';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();
    const handleLogin = () => {
 // Send login request to the backend
 axios
 .post('http://localhost:8001/login', { email, password })
 .then(response => {
    setMessage(response.data.message);
    const { username, email, token} = response.data;
    localStorage.setItem('username', username);
    localStorage.setItem('email', email);
    localStorage.setItem('token', token);
// Redirect to homepage using navigate
    navigate('/'); // Replace '/' with the homepage URL if needed
 })
 .catch(error =>
{
 console.error(error);
 setMessage('Error logging in. Please try again.');
 });
 };
return (
 <div>
 <h2>Login</h2>
 <div>
 <input
 type="email"
 placeholder="Email"
 value={email}
 onChange={e => setEmail(e.target.value)}
 />
 <input
 type="password"
 placeholder="Password"
 value={password}
 onChange={e => setPassword(e.target.value)}
 />
 <button onClick={handleLogin}>Login</button>
    {message && <p>{message}</p>}
 </div>
 </div>
 );
 }
export default Login;