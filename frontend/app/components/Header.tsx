// components/Header.tsx
import React from 'react';
import Link from 'next/link';
import SignInButton from './SignInButton';

const Header: React.FC = () => {
  return (
    <header className="bg-blue-600 text-white px-6 py-4">
      <div className="container mx-auto flex justify-between items-center">
        <a href="/" className="text-2xl font-semibold">
          Casual Progress
        </a>
        <nav>
          <ul>
            <li>
              <Link href="/settings" className="ml-4">
                Settings
              </Link>
            </li>
            <li>
              <SignInButton/>              
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
