import express from 'express'
import dotenv from 'dotenv'
import cookieParser from 'cookie-parser'
import { connectDB } from './db/db.js';
import authRoutes from './route/authRoutes.js';
import cors from 'cors'

const app = express();

dotenv.config();
app.use(cors({
    origin: "http://localhost:5173", // or whatever port Vite is running
    methods: ["GET", "POST", "PUT", "DELETE"],
    credentials: true, // if you’re sending cookies/auth headers
  }))
app.use(express.json());
app.use(cookieParser());


app.use('/auth', authRoutes)

const PORT = process.env.PORT
app.listen(PORT, () => {
    connectDB()
    console.log(`Server is running on http://localhost:${PORT}`)
})