import React from 'react';
import './Login.css';

function Signup() {

  return (
    <div className='login-container'>
      <h1>Grocery Central</h1>
      <form className="login-form" method='POST' action="/api/user/login">
        <h1>Sign Up</h1>
        <label htmlFor='login'>Username or Email</label>
        <input name='login' type='text' />

        <label htmlFor='password'>Password</label>
        <input name='password' type='text' />

        <label htmlFor='confPassword'>Confirm Password</label>
        <input name='confPassword' type='text' />

        <button type='submit' className="submit-btn">Create Account</button>
        <a href='/signup' className='embedded-link'>
          <button type='button' href='/signup' className="redirect-btn">Go Back</button>
        </a>
      </form>
    </div>
  )
}

export default Signup;
