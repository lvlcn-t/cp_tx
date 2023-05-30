import React from 'react';

const ArrowRightOnRectangleIcon: React.FC<React.SVGProps<SVGSVGElement>> = (
  props
) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="currentColor"
      {...props}
    >
      <path d="M16 12l-9-8v16z" />
      <path d="M22 12l-4-4v3H2v2h16v3z" fillOpacity=".5" />
    </svg>
  );
};

export default ArrowRightOnRectangleIcon;
