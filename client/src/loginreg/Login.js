import React from 'react';
import './Login.css';

function Login() {

  return (
    <div className='login-container'>
      <h1>Grocery Central</h1>
      <form className="login-form" method='POST' action="/api/user/login">
        <h1>Sign in</h1>
        <label htmlFor='login'>Username or Email</label>
        <input name='login' type='text' />

        <label htmlFor='password'>Password</label>
        <input name='password' type='text' />

        <div className='form-flex'>
          <input name='remember' type='checkbox' />
          <h2>Remember Me</h2>
        </div>
        <button type='submit' className="submit-btn">Continue</button>
        <h2><hr></hr>or<hr></hr></h2>
        <a href='/signup' className='embedded-link'>
          <button type='button' href='/signup' className="redirect-btn">Create Account</button>
        </a>
      </form>
    </div>
  )
}

export default Login;
