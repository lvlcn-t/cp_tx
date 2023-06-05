// components/Header.tsx
import React from 'react';
import Link from 'next/link';
import SignInButton from './SignInButton';

const Header: React.FC = () => {
  return (
    <header className="bg-slate-800 text-white px-6 py-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-2xl font-semibold inline-block">
          Casual Progress
        </Link>
        <nav className="inline-block">
          <ul>
            <li className="inline-block">
              <Link href="/settings" className="ml-4">
                Settings
              </Link>
            </li>
            <li className="inline-block">
              <SignInButton/>              
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
