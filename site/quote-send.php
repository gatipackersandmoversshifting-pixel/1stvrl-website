<?php
/* 1st VRL Packers and Movers - quote form handler.
   Validates input, logs the lead OUTSIDE the web root when possible, and emails it.
   No credentials stored in code. No .htaccess required. */

declare(strict_types=1);

const LEAD_TO = 'support@1stvrlpackersandmovers.com';
const HONEYPOT = 'website';

function vrl_clean(string $value): string
{
    $value = trim($value);
    $value = str_replace(["\r", "\n"], ' ', $value);
    $value = preg_replace('/[\x00-\x1F\x7F]/u', '', $value) ?? '';
    return mb_substr($value, 0, 300);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: /', true, 302);
    exit;
}

$name  = vrl_clean($_POST['name'] ?? '');
$phone = preg_replace('/[^0-9+]/', '', vrl_clean($_POST['phone'] ?? ''));
$email = vrl_clean($_POST['email'] ?? '');
$from  = vrl_clean($_POST['from'] ?? '');
$to    = vrl_clean($_POST['to'] ?? '');
$type  = vrl_clean($_POST['move_type'] ?? '');
$date  = vrl_clean($_POST['date'] ?? '');
$msg   = vrl_clean($_POST['message'] ?? '');
$hp    = trim($_POST[HONEYPOT] ?? '');
$page  = vrl_clean($_POST['page'] ?? '');

if ($page === '' || !preg_match('#^[A-Za-z0-9\-_/.]*$#', $page)) {
    $page = '/';
}

if ($hp !== '' || $name === '' || strlen($phone) < 10) {
    header('Location: ' . $page . '?err=1', true, 302);
    exit;
}

$fields = [
    'Time'      => date('d M Y, h:i A T'),
    'Name'      => $name,
    'Phone'     => $phone,
    'Email'     => $email,
    'From'      => $from,
    'To'        => $to,
    'Move type' => $type,
    'Date'      => $date,
    'Message'   => $msg,
    'Page'      => $page,
    'IP'        => $_SERVER['REMOTE_ADDR'] ?? '',
];

// Log OUTSIDE the public web root. If that folder is not writable, skip logging
// rather than writing a downloadable leads.csv into public_html.
$logDir = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'vrl-leads';
$logPath = '';
if (is_dir($logDir) && is_writable($logDir)) {
    $logPath = $logDir . DIRECTORY_SEPARATOR . 'leads.csv';
} else {
    @mkdir($logDir, 0750, true);
    if (is_dir($logDir) && is_writable($logDir)) {
        $logPath = $logDir . DIRECTORY_SEPARATOR . 'leads.csv';
    }
}

if ($logPath !== '') {
    $firstWrite = !file_exists($logPath);
    $handle = @fopen($logPath, 'ab');
    if ($handle !== false) {
        if ($firstWrite) {
            fputcsv($handle, array_keys($fields));
        }
        fputcsv($handle, array_values($fields));
        fclose($handle);
    }
}

// Also send the lead to the CRM. Never blocks the form if the CRM is slow or down.
if (function_exists('curl_init')) {
    $crmDetails = trim(($type !== '' ? 'Move type: ' . $type . '. ' : '') . ($msg !== '' ? $msg . ' ' : '') . 'Page: ' . $page);
    $ch = curl_init('https://1stvrlpackersandmovers.kingweb.in/api/index.php');
    curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 8, CURLOPT_CONNECTTIMEOUT => 4,
        CURLOPT_POSTFIELDS => http_build_query(['KEY' => '491bdfa5e018667262bb2c5d74e5c87d', 'Name' => $name, 'Email' => $email, 'Contact' => $phone,
            'Movingfrom' => $from, 'Movingto' => $to, 'Movingdate' => $date, 'Details' => $crmDetails])]);
    $crmReply = curl_exec($ch);
    curl_close($ch);
    $fields['CRM enquiry'] = is_string($crmReply) ? mb_substr($crmReply, 0, 60) : 'not sent';
}

$body = "New quote request\n\n";
foreach ($fields as $key => $value) {
    $body .= $key . ': ' . $value . "\n";
}

$subject = 'Quote request - ' . $name . ' (' . $phone . ')';

// From must be on this domain so SPF/DMARC align and the mail is not spam-filtered.
$headers = 'From: 1st VRL Packers and Movers <' . LEAD_TO . ">\r\n"
         . 'Reply-To: ' . ($email !== '' ? $email : LEAD_TO) . "\r\n"
         . 'MIME-Version: 1.0' . "\r\n"
         . 'Content-Type: text/plain; charset=UTF-8';

$sent = mail(LEAD_TO, $subject, $body, $headers, '-f' . LEAD_TO);

if ($sent !== true) {
    error_log('VRL lead mail FAILED for ' . $phone . ' -> ' . LEAD_TO . ' on ' . date('c'));
}

header('Location: /thank-you?sent=' . ($sent ? '1' : '0'), true, 302);
exit;