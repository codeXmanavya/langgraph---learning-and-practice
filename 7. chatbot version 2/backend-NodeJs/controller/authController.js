import bcrypt from "bcryptjs";
import User from "../model/UserModel.js";

export const postSignup = async (req,res) => {
    try {

        const {email , password} = req.body;

        const salt = bcrypt.genSaltSync(10);
        const hashPassword = bcrypt.hashSync(password, salt);

        const user = new User({
            email,
            password:hashPassword
        });

        await user.save();

        res.status(200).json({message:'User created successfully'});

    } catch (error) {
        res.status(401).json({errors:[{msg:error.msg}]});
    }
}

export const postSignin = async (req,res) => {
    try {

        const {email, password} = req.body;
        const user = await User.findOne({email})
        if (!user){
            throw new Error('User not found');
        } 

        const existingUser = await bcrypt.compare(password, user.password)

        if(!existingUser){
            res.status(400).json({errors:[{msg:'Invalid email or password'}]})
        }

        res.status(200).json({message:"User logged in succussfullly",username:email})

        
    } catch (error) {
        return res.status(401).json({errors:[{msg:error.msg}]});
    }

}

export const postSignout = () => {

}