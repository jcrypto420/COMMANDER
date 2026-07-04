import './globals.css';

export const metadata = {
  title: 'Commander Mission Control',
  description: 'Private mission-control dashboard for Josh and Commander.',
  manifest: '/manifest.webmanifest',
  icons: {
    icon: '/mission-control-icon-192.png',
    apple: '/apple-touch-icon.png',
  },
};

export const viewport = {
  themeColor: '#050507',
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
