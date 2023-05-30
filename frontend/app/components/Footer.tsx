// components/Footer.tsx
import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-blue-600 text-white px-6 py-4 mt-8">
      <div className="container mx-auto text-center">
        Discord Bot Dashboard © {new Date().getFullYear()}
      </div>
    </footer>
  );
};

export default Footer;
