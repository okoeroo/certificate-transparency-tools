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


        print('CAA example based on certificate transparency logs (=current certificate usage):');
        print ("<br>\n");
        print ("<br>\n");

        /* Input is clean, start processing */

        $cmd = $GEN_TLSA_SH. " --caa --domain " . $domain;
        exec($cmd, $output);

        foreach ($output as &$value) {
            print($value.'<br>');
        }
        print ("<br>");


        $data = array("domain" => $domain);
        $data_string = json_encode($data);

        $ch = curl_init("http://localhost:5000/caahunter");
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
        curl_setopt($ch, CURLOPT_POST,count($data_string));
        curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array(
            'Content-Type: application/json',
            'Content-Length: ' . strlen($data_string))
        );
        $result = curl_exec($ch);
        $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        print '<br>';
        /* print $result; */
        $resj = json_decode($result, true);

        /* print '<br>'; */
        print "Currently implemented CAA records at " . $domain;
        print '<br>';
        foreach ($resj as $dns_rr) {
            /* print $dns_rr-> */
            print '<br>';
            print $dns_rr['fqdn'] . " " . $dns_rr['r_type'] . " " .$dns_rr['value'];

        }

        /* header("refresh:3;url=index.html"); */
        return;
    }
?>
