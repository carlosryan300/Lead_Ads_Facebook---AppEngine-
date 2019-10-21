CREATE TABLE table_leads_facebook(
            email NVARCHAR(300) NOT NULL,
            nome NVARCHAR(200) NOT NULL,
            fb_leadgen_id NVARCHAR(40) NOT NULL,
            fb_form_id NVARCHAR(40) NOT NULL,
            fb_page_id NVARCHAR(40) NOT NULL,
            fb_created_time_stamp INT NOT NULL,
            id_vtex NVARCHAR(100) NOT NULL,
            href_vtex NVARCHAR(200) NOT NULL,
            documentId_vtex NVARCHAR(100) NOT NULL,
            xCodigoParceria INT NOT NULL,
            xCodigoParceriaOrigem INT NOT NULL,
            date_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);
        


INSERT INTO table_leads_facebook(
    email,
    nome,
    fb_leadgen_id,
    fb_form_id,
    fb_page_id,
    fb_created_time_stamp,
    id_vtex,
    href_vtex,
    documentId_vtex,
    xCodigoParceria,
    xCodigoParceriaOrigem,
    date_time
)VALUES(
    {email},
    {nome},
    {fb_leadgen_id},
    {fb_form_id},
    {fb_page_id},
    {fb_created_time_stamp},
    {id_vtex},
    {href_vtex},
    {documentId_vtex},
    10101698,
    10101698,
    {date_time},
)










email                     | STRING
nome                      | STRING
fb_leadgen_id             | INT
fb_form_id                | INT 
fb_page_id                | INT 
fb_created_time_stamp     | INT 
id_vtex                   | STRING
href_vtex                 | STRING
documentId_vtex           | STRING
xCodigoParceria           | INT 
xCodigoParceriaOrigem     | INT 
date_time                 | TIMESTAMP      