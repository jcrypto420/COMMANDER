import './globals.css';

export const metadata = {
  title: 'Commander Mission Control',
  description: 'Private mission-control dashboard for Josh and Commander.'
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <meta httpEquiv="refresh" content="120" />
      </head>
      <body>{children}</body>
    </html>
  );
}
