const express = require("express");
const cors = require("cors");
const app = express();
require("dotenv").config();

const flashcardRoutes = require("./routes/flashcards");

app.use(cors());
app.use(express.json());
app.use("/api/flashcards", flashcardRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
