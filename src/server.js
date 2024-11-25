const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 8070;

// Setup storage engine using multer
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  },
});

const upload = multer({ storage: storage });

// Ensure uploads directory exists
if (!fs.existsSync('uploads')) {
  fs.mkdirSync('uploads');
}

app.use(express.json());

app.post('/predict', upload.single('photo'), (req, res) => {
  const imageDetails = {
    filename: req.file.filename,
    path: req.file.path,
    mimetype: req.file.mimetype,
    size: req.file.size,
  };

  // Read the current content of images.json file
  fs.readFile('images.json', (err, data) => {
    let json = [];
    if (!err && data.length > 0) {
      json = JSON.parse(data);
    }

    // Add new image details to the array
    json.push(imageDetails);

    // Write updated content back to images.json file
    fs.writeFile('images.json', JSON.stringify(json, null, 2), (err) => {
      if (err) {
        console.error('Error writing to file', err);
        return res.status(500).send('Error saving image details');
      }

      res.json({ message: 'Image uploaded successfully', imageDetails });
    });
  });
});

app.listen(port, () => {
  console.log(`Server running at http://10.70.22.127:${3020}`);
});
