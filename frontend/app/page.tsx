"use client"
import React, { useState } from 'react'



const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault()
    // Handle form submission here: validate inputs, call APIs, etc.
  }

  return (
    <>
      
    </>
  )
}

export default LoginPage
