//Criando o nodemailer transporte
const transporter = nodemailer.createTransport({
    host: 'smtp.gmail.com',
    port: 465,
    secure: true,
    auth: {
        user: `${process.env.EMAIL_USER}`,
        pass: `${process.env.EMAIL_PASS}`
    },
    tls: {
        rejectUnauthorized: false
    }
});

async function enviarEmail(user, resetToken) {
    resetLink = `http://localhost:8081/reset-password?token=${resetToken}&email=${user.email}`;
    await transporter.sendMail({
        from: `"Equipe Poligera" <${process.env.EMAIL_USER}>`,
        to: user.email,
        subject: "Recuperação de senha",
        html: `<p>Olá ${user.name},</p>
                <p>Você solicitou a redefinição da sua senha.</p>
                <p>Clique no link abaixo para criar uma nova senha:</p>
                <a href="${ resetLink }">
                    Redefinir senha
                </a>
                <p>Se você não fez essa solicitação, ignore este e-mail. Sua senha permanecerá inalterada.</p>`
    });
}

