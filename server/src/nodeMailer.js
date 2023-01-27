const nodeMailer = require('nodemailer');

module.exports = {
    sendVerifyEmail: async function(email, subject, text) {
        try {
            const transporter = nodeMailer.createTransport({
                host: process.env.NMHOST,
                service: process.env.NMSERVICE,
                port: Number(process.env.NMEMAIL_PORT),
                secure: Boolean(process.env.NMSECURE),
                auth: {
                    user: process.env.NMUSER,
                    pass: process.env.NMPASS
                }
            });

            await transporter.sendMail({
                from: process.env.NMUSER,
                to: email,
                subject: subject,
                text: text
            });
            console.log('Email sent successfully');
            return;
        } catch (err) {
            console.log(`${err.name}: ${err.message}`);
            return `${err.name}: ${err.message}`;
        }
    },
};