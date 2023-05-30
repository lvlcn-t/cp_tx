"use client"
import React, { useState } from 'react'
import Header from './components/Header'
import Footer from './components/Footer'

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault()
    // Handle form submission here: validate inputs, call APIs, etc.
  }

  return (
    <div>
      <Header/>
      <main>
        <div className="flex items-center justify-center h-screen bg-gray-100">
          <div className="w-full max-w-md">
            <form onSubmit={handleSubmit} className="bg-white shadow-lg rounded px-12 pt-6 pb-8 mb-4">
              <div className="text-gray-800 text-2xl flex justify-center border-b-2 py-2 mb-4">
                Login
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
                  Email
                </label>
                <input 
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  id="email"
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div className="mb-6">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
                  Password
                </label>
                <input 
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" 
                  id="password"
                  type="password"
                  placeholder="**********"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              <div className="flex items-center justify-between">
                <button 
                  className="px-4 py-2 rounded text-white inline-block shadow-lg bg-blue-500 hover:bg-blue-600 focus:bg-blue-700" 
                  type="submit">
                  Sign In
                </button>
              </div>
            </form>
          </div>
        </div>
      </main>
      <Footer/>
    </div>
    
  )
}

export default LoginPage
