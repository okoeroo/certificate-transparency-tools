<?php
    /* require_once 'globals.php'; */

    $TOPDIR = '/var/www/caa.koeroo.net/';
    $GEN_TLSA_SH=$TOPDIR.'domain-2-CAA-proposal.py';
    $PROCESS_POST_PHP="process_post.php";


    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        /* Start processing */
        $domain = trim($_POST["domain"]);

        if(preg_match('/[^\.a-zA-Z\-0-9]/i', $domain)) {
            header("refresh:4;url=index.php");
            print("Not a valid FQAN. No special characters allowed.\n");
            print("You typed: ");
            print($domain);
            return;
        }


        print('CAA example:');
        print ("<br>\n");
        print ("<br>\n");

        /* Input is clean, start processing */

        $cmd = $GEN_TLSA_SH. " --caa --domain " . $domain;
        exec($cmd, $output);

        foreach ($output as &$value) {
            print($value.'<br>');
        }
        print ("<br>");

        return;
    }
?>
