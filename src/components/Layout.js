import React from 'react';
import { Box, CssBaseline, Toolbar } from '@mui/material';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import { useAuth } from '../context/AuthContext';

const drawerWidth = 240;

const Layout = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  if (!isAuthenticated) {
    return <>{children}</>;
  }

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <Navbar drawerWidth={drawerWidth} handleDrawerToggle={handleDrawerToggle} />
      <Sidebar 
        drawerWidth={drawerWidth} 
        mobileOpen={mobileOpen} 
        handleDrawerToggle={handleDrawerToggle} 
      />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default Layout;
