import React from 'react';
import './Login.css';

function Login() {

  return (
    <div className='login-container'>
      <h1>Grocery Central</h1>
      <form className="login-form" method='POST' action="/api/user/login">
        <h1>Sign in</h1>
        <label htmlFor='email'>Email or Username</label>
        <input name='email' type='text' />
        <label htmlFor='email'>Password</label>
        <input name='password' type='text' />
        <div className='form-flex'>
          <input name='password' type='checkbox' />
          <h2>Remember Me</h2>
        </div>
        <button type='submit' className="submit-btn">Continue</button>
      </form>
    </div>
  )
}

export default Login
