export const metadata = {
  title: 'DataIntel — YouTube Analytics Platform',
  description: 'Ask any question about your YouTube analytics. Get instant interactive dashboards powered by AI.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, padding: 0, background: '#0C0904' }}>
        {children}
      </body>
    </html>
  );
}
