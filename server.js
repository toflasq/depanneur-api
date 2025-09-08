const express = require("express");
const cors = require("cors");
const fs = require("fs");

const app = express();
app.use(cors());

const PORT = process.env.PORT || 3000;

// Charger le JSON
const rawData = fs.readFileSync("data.json");
const database = JSON.parse(rawData);

// Route d’accueil
app.get("/", (req, res) => {
  res.send("🚀 API Dépanneur en ligne !");
});

// Route pour récupérer toutes les unités
app.get("/units", (req, res) => {
  res.json(database.units);
});

// Exemple : filtrer par catégorie
app.get("/units/:category", (req, res) => {
  const cat = req.params.category.toLowerCase();
  const results = database.units.filter(u =>
    u.category.toLowerCase().includes(cat)
  );
  res.json(results);
});

// Route pour modules complémentaires
app.get("/modules", (req, res) => {
  res.json(database.modules || []);
});

app.listen(PORT, () => {
  console.log(`✅ Serveur lancé sur http://localhost:${PORT}`);
});
