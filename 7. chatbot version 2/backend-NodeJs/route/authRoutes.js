import express from 'express'
import { postSignup, postSignin, postSignout } from '../controller/authController.js';
import { validateSignup, validateSignin } from '../middleware/authValidator.js';

const authRouter = express.Router();

authRouter.post('/signup', validateSignup, postSignup);
authRouter.post('/signin', validateSignin, postSignin);
authRouter.post('/signout', postSignout);

export default authRouter;