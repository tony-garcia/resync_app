import {
  Box,
  Card,
  CardActions,
  CardContent,
  Grid,
  IconButton,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';

import { Edit, Delete } from '@mui/icons-material';

import MoleculeStructure from './moleculeStructure';

function StructureViewer({ compounds }) {
  return (
    <Box sx={{ margin: '30px' }}>
      <Grid container spacing={2}>
        {compounds.map((compound) => (
          <Grid key={compound.id} size={4}>
            <Card>
              <CardContent sx={{ display: 'flex' }}>
                <div style={{ backgroundColor: '#fff', width: '250px', margin: 'auto' }}>
                  <MoleculeStructure id={compound.id} structure={compound.smiles} svgMode />
                </div>
                <div>
                  <List dense>
                    {Object.entries(compound.data).map(([prop, value]) => (
                      <ListItem key={compound.id}>
                        <ListItemText primary={prop} secondary={value} />
                      </ListItem>
                    ))}
                  </List>
                </div>
              </CardContent>
              <CardActions>
                <IconButton edge="end" onClick={() => console.log(compound.compound_id)}>
                  <Edit />
                </IconButton>
                <IconButton edge="end" onClick={() => console.log(compound.compound_id)}>
                  <Delete />
                </IconButton>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default StructureViewer;
