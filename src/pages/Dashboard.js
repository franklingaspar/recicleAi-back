import React, { useState, useEffect } from 'react';
import { 
  Typography, 
  Grid, 
  Paper, 
  Box, 
  CircularProgress,
  Card,
  CardContent,
  CardHeader
} from '@mui/material';
import BusinessIcon from '@mui/icons-material/Business';
import PeopleIcon from '@mui/icons-material/People';
import RecyclingIcon from '@mui/icons-material/Recycling';
import { useAuth } from '../context/AuthContext';
import companyService from '../services/companyService';
import userService from '../services/userService';
import collectionService from '../services/collectionService';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    companies: 0,
    users: 0,
    collections: 0,
    pendingCollections: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [companies, users, collections] = await Promise.all([
          companyService.getCompanies(),
          userService.getUsers(),
          collectionService.getCollections()
        ]);

        const pendingCollections = collections.filter(
          collection => collection.status === 'pending'
        );

        setStats({
          companies: companies.length,
          users: users.length,
          collections: collections.length,
          pendingCollections: pendingCollections.length
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="50vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        Bem-vindo, {user?.name || user?.email}!
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={3}>
            <CardHeader
              title="Empresas"
              avatar={<BusinessIcon color="primary" />}
            />
            <CardContent>
              <Typography variant="h3" align="center">
                {stats.companies}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={3}>
            <CardHeader
              title="Usuários"
              avatar={<PeopleIcon color="primary" />}
            />
            <CardContent>
              <Typography variant="h3" align="center">
                {stats.users}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={3}>
            <CardHeader
              title="Coletas Totais"
              avatar={<RecyclingIcon color="primary" />}
            />
            <CardContent>
              <Typography variant="h3" align="center">
                {stats.collections}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={3}>
            <CardHeader
              title="Coletas Pendentes"
              avatar={<RecyclingIcon color="warning" />}
            />
            <CardContent>
              <Typography variant="h3" align="center">
                {stats.pendingCollections}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
