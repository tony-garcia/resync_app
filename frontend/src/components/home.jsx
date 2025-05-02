import React, { useState } from "react";
import {
  Button,
  Box,
  Card,
  CardContent,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Paper,
  TextField,
  Typography,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import axios from "axios";

import { useAPI } from "../../hooks";
import { applyType } from '../utils';


const initialFormData = {
  id: null,
  smiles: '',
};

function Home() {
  const [formOpen, setFormOpen] = useState(false);
  const [formData, setFormData] = useState(initialFormData);
  // State for properties
  const [properties, setProperties] = useState([]);

  // State for current input fields
  const [currentProperty, setCurrentProperty] = useState('');
  const [currentValue, setCurrentValue] = useState('');

  const { data, isLoading, refresh, error } = useAPI({ url: '/api/compounds/' }, {});

  const handleOpenForm = () => setFormOpen(true);
  const handleCloseForm = () => setFormOpen(false);

  const handleChange = ({ target }) => {
    const { value } = target;
    setFormData((prevData) => ({
      ...prevData,
      smiles: value
    }))
  };

  // Function to add a new property
  const addProperty = () => {
    if (currentProperty.trim() !== '') {
      // Create new property object
      const newProperty = {
        id: Date.now(),
        name: currentProperty,
        value: currentValue,
      };

      // Add to properties array
      setProperties([...properties, newProperty]);

      // Reset input fields
      setCurrentProperty('');
      setCurrentValue('');
    }
  };

  // Function to remove a property
  const removeProperty = (id) => {
    setProperties(properties.filter((property) => property.id !== id));
  };

  const createCompound = async (data) => {
    try {
      const response = await axios.post('/api/compounds/', data);
      // reload compound data
      refresh();
    } catch (error) {
      if (error.response) {
        console.error('An error occurred!');
        console.error('data:', error.response.data);
        console.error('status:', error.response.status);
      }
    } finally {
      // Close the modal after submission
      handleCloseForm();
      // Reset form
      setFormData(initialFormData);
      setProperties([]);
    }
  }

  const updateCompound = async (data) => {
    console.log('update')
    console.log({ data })
  }

  const handleSubmit = (event) => {
    event.preventDefault();

    // Create object from properties
    const compoundData = {};
    properties.forEach((prop) => {
      compoundData[prop.name] = applyType(prop.value);
    });
    const payLoad = { ...formData, data: compoundData };
    if (payLoad.id) {
      updateCompound(payLoad);
    } else {
      createCompound(payLoad);
    }
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
            <Card>
              <CardContent>
                <TextField
                  name="smiles"
                  label="SMILES String"
                  value={formData.smiles}
                  onChange={handleChange}
                  fullWidth
                  required
                  margin="dense"
                />
                <Box mb={3} display="flex" alignItems="flex-end">
                  <TextField
                    label="Property Name"
                    value={currentProperty}
                    onChange={(e) => setCurrentProperty(e.target.value)}
                    variant="outlined"
                    fullWidth
                    sx={{ mr: 1 }}
                  />
                  <TextField
                    label="Property Value"
                    value={currentValue}
                    onChange={(e) => setCurrentValue(e.target.value)}
                    variant="outlined"
                    fullWidth
                    sx={{ mr: 1 }}
                  />
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<AddIcon />}
                    onClick={addProperty}
                    sx={{ height: 56 }}
                  >
                    Add
                  </Button>
                </Box>
                <Paper variant="outlined" sx={{ mb: 3 }}>
                  {properties.length > 0 ? (
                    <List>
                      {properties.map((property, index) => (
                        <React.Fragment key={property.id}>
                          {index > 0 && <Divider />}
                          <ListItem
                            secondaryAction={
                              <IconButton
                                edge="end"
                                aria-label="delete"
                                onClick={() => removeProperty(property.id)}
                              >
                                <DeleteIcon />
                              </IconButton>
                            }
                          >
                            <ListItemText primary={property.name} secondary={property.value} />
                          </ListItem>
                        </React.Fragment>
                      ))}
                    </List>
                  ) : (
                    <Box py={3} textAlign="center">
                      <Typography color="textSecondary">
                        No properties added yet. Add some above!
                      </Typography>
                    </Box>
                  )}
                </Paper>
              </CardContent>
            </Card>
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
