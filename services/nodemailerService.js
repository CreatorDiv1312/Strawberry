const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: "tanmaycloud251@gmail.com", 
        pass: "niat hidw vyjp ywfd", 
    },
});


const sendMail = async ( subject, text) => {
    const mailOptions = {
        from: "tanmaycloud251@gmail.com", 
        to: "tanmaycloud251@gmail.com",
        subject, // Email subject
        text, //body
    };

    try {
        const info = await transporter.sendMail(mailOptions);
        console.log(`Email sent: ${info.response}`);
        return info;
    } catch (error) {
        console.error(`Error sending email: ${error.message}`);
        throw error;
    }
};

module.exports = sendMail;