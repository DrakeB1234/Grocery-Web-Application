const nodeMailer = require('nodemailer');

module.exports = {
    sendVerifyEmail: async function(email, subject, text) {
        try {
            const transporter = nodeMailer.createTransport({
                host: process.env.HOST,
                service: process.env.SERVICE,
                post: Number(process.env.EMAIL_PORT),
                secure: Boolean(process.env.SECURE),
                auth: {
                    user: process.env.USER,
                    pass: process.env.PASS
                }
            });

            await transporter.sendMail({
                from: process.env.USER,
                to: email,
                subject: subject,
                text: text
            });
            console.log('Email sent successfully');
            return;
        } catch (err) {
            console.log('Failed to send email');
            return `${err.name}: ${err.message}`;
        }
    },
};