import React, { useEffect, useState } from 'react';

function Homepage() {
    const [userData, setUserData] = useState(null);
    useEffect(() => {
    // Fetch user data from the API endpoint
        fetch('http://localhost:8001/api/user', {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
    })
    .then(response => response.json())
    .then(data => setUserData(data))
    .catch(error => console.error(error));
    }, []);
    const username = localStorage.getItem('username');
    const email = localStorage.getItem('email');
return (
 <div>
 <h1>Welcome to the Homepage</h1>
 {userData && (
    <p>
        Welcome {username}, {email} to the homepage!
    </p>
 )}
 </div>
 );
 }

export default Homepage;