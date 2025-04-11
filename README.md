## 📌 Description

Cette branche ajoute les premiers endpoints liés à la gestion des événements dans l'application **Mobile Musician**.

🔧 Ces endpoints sont fonctionnels mais **ne nécessitent pas encore d’authentification**.  
Ils sont utiles pour les tests initiaux avant intégration complète avec le système d'utilisateur connecté.

---

## 🚀 Endpoints disponibles

### ➕ Créer un événement
**POST** `/api/v1/events`

- Crée un événement avec des données JSON
- Utilise un `organizer_id` de test (UUID fixe)

---

### 📋 Lister tous les événements
**GET** `/api/v1/events`

- Retourne une liste de tous les événements créés

---

### 🔍 Détail d’un événement
**GET** `/api/v1/events/{id}`

- Retourne les informations détaillées d’un événement spécifique

---

## ✅ À venir

- 🔐 Ajout de l'authentification avec `get_current_user`
- 🧍 Participation à un événement (`POST /events/{id}/participate`)
- 🗑️ Suppression ou modification des événements
- ✅ Tests unitaires des endpoints

---

## 🧪 Test local

```bash
uvicorn app.main:app --reload --port 8001
