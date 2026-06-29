import './globals.css';

export const metadata = {
  title: 'Commander Mission Control',
  description: 'Private mission-control dashboard for Josh and Commander.'
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
