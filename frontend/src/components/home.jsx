import { useState } from "react";
import { useAPI } from "../../hooks";

import {
  Button,
  Typography,
  TextField,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
} from '@mui/material';

const initialFormData = {
  smiles: '',
  data: '',
};

function Home() {
  const [formOpen, setFormOpen] = useState(false);
  const [formData, setFormData] = useState(initialFormData);

  const { data, isLoading, error } = useAPI({ url: '/api/compounds/' }, {});

  const handleOpenForm = () => setFormOpen(true);
  const handleCloseForm = () => setFormOpen(false);

  const handleChange = (event) => {
    const { name, value, checked, type } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value
    }))
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Here you would typically send the data to your backend
    console.log('Form submitted:', formData);

    // Close the modal after submission
    handleCloseForm();

    // Reset form
    setFormData(initialFormData);
  };

  return (
    <>
      <Typography style={{ fontSize: '2em' }} align="center" variant="h1">
        Compound Manager
      </Typography>
      <div style={{ textAlign: "center", margin: '30px' }}>
        <Button variant="contained" onClick={handleOpenForm}>Add Compound</Button>
      </div>

      <Dialog open={formOpen} onClose={handleCloseForm} maxWidth="md">
        <DialogTitle>Add Compound</DialogTitle>

        <form onSubmit={handleSubmit}>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} sm={6}>
                <TextField
                  name="smiles"
                  label="SMILES String"
                  value={formData.smiles}
                  onChange={handleChange}
                  fullWidth
                  required
                  margin="dense"
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  name="data"
                  label="Data"
                  onChange={handleChange}
                  fullWidth
                  required
                  margin="dense"
                />
              </Grid>
            </Grid>
          </DialogContent>

          <DialogActions sx={{ px: 3, pb: 2 }}>
            <Button onClick={handleCloseForm} color="primary">
              Cancel
            </Button>
            <Button type="submit" variant="contained" color="primary">
              Submit
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </>
  );
}

export default Home;
