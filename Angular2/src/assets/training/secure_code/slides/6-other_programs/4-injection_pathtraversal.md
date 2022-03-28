### Filenames (Including Path Traversal)

Technically, a “**pathname**” is a sequence of bytes that describes how to find a filesystem object. On Unix-like systems, including Linux, Android, MacOS, and iOS, a pathname is a sequence of one or more filenames separated by one or more “**/**”. On Windows systems, a pathname is more complicated but the idea is the same. In practice, many people use the term “filename” to refer to pathnames.

Pathnames are often at least partly controlled by an untrusted user. For example, it is often useful to use filenames as a key to identify relevant data, but this can lead to untrusted users controlling filenames. Another example is when monitoring or managing shared systems (e.g., virtual machines or containerized filesystems); in this case, an untrusted monitoree controls filenames. Even when an attacker should not be able to gain this kind of control, it is often important to counter this kind of problem as a defense-in-depth measure, to counter attackers who gain a small amount of control.

#### Path Traversal

An obvious case is that systems are often not supposed to allow access outside of some directory (e.g., a “document root” of a web server). For example, if a program tries to access a path that is a concatenation of “**trusted_root_path**” and “**username**”, the attacker might be able to create a username “.**./../../mysecrets**” and foil the limitations. This vulnerability, where an attacker can create filenames that traverse outside where it is supposed to, is so common that it has a name: *directory traversal vulnerabilities*. As always, use a very limited allowlist for information that will be used to create filenames. If your web application’s allowlist does not include “**.**”, “**/**”, “**~**”, and “**&#92;**”, on most systems it is significantly harder to traverse outside the intended directory root. Another common solution is to convert a relative path into a normalized absolute path in a way that eliminates all “**..**” uses and then ensure that the resulting path is still in the correct region of the filesystem.

STORY TIME: SaltStack

An example of a directory traversal vulnerability is [CVE-2020-11652](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-11652), a vulnerability in the SaltStack. SaltStack is a configuration management and orchestration tool for managing multi-computer infrastructure. In this vulnerability, a method failed to properly sanitize an input parameter, allowing “**..**” elements that were used to create a filename. The result was that attackers could cause entire sets of machines to execute commands of their choosing.

Path traversal is such a common cause of security vulnerabilities that it is 2019 CWE Top 25 #10. It is also identified as [CWE-22](https://cwe.mitre.org/data/definitions/22.html), *Improper Limitation of a Pathname to a Restricted Directory (‘Path Traversal’)*.

#### Windows Pathnames

Microsoft Windows pathnames can be extremely difficult to deal with securely. Windows pathname interpretations vary depending on the version of Windows and the API used (many calls use **CreateFile** which supports the pathname prefix “**\\.&#92;**” - and these interpret pathnames differently than the other calls that do not). Perhaps most obviously, “**letter:**” and “**\\server\share...**” have a special meaning in Windows. A nastier issue is that there are reserved filenames, whose form depends on the API used and the local configuration. The built-in reserved device names are as follows: CON, PRN, AUX, NUL, COM1, COM2, COM3, COM4, COM5, COM6, COM7, COM8, COM9, LPT1, LPT2, LPT3, LPT4, LPT5, LPT6, LPT7, LPT8, and LPT9. Even worse, drivers can create more reserved names - so you actually cannot know ahead-of-time what names are reserved. You should avoid creating filenames with reserved names, both with and without an extension; if an attacker can trick the program into reading/writing the name (e.g., **com1.txt**), it may (depending on API) cause read or write to a device instead of a file. In this case, even simple alphanumerics can cause disaster and be interpreted as metacharacters - this is rare, since usually alphanumerics are safe. Windows supports “**/**” as a directory separator, but it conventionally uses “**&#92;**” as the directory separator (which is annoying because **&#92;** is widely used as an escape character). In Windows, don’t end a file or directory name with a space or period; the underlying filesystem may support it, but the Windows shell and user interface generally do not. For more details, check the Microsoft Windows documentation on [*Naming Files, Paths, and Namespaces*](https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file?redirectedfrom=MSDN).

#### Unix/Linux Pathnames

Filenames and pathnames on Unix-like systems are not always easy to deal with either. On most Unix-like systems, a filename can be any sequence of bytes that does not include **\0** (the terminator) or slash. One common misconception is that Unix filenames are a string of characters. Unix filenames are not a string of one or more characters; they are merely a sequence of bytes, so a filename does not need to be a legal sequence of characters. For example, while it is a common convention to interpret filenames as a UTF-8 encoding of characters, most systems do not actually enforce this. Indeed, they tend to enforce nothing, so many problematic filenames can be created, including filenames with spaces (or only spaces), control characters (including newline, tab, escape, etc.), bytes that are not legal UTF-8, or

including a leading “**-**” (the marker for command options). These problematic filenames can cause trouble later.

Some potential problems with filenames are specific to the shell, but filename problems are not limited to the shell. A common problem is that “**-**” is the option flag for many commands, but it is a legal beginning of a filename.

A simple solution is to prefix all globs or filenames where needed with “**./**” so that they cannot begin with “**-**”. So for example, never use “**&#42;.pdf**” to refer to a set of PDFs if an attacker might influence a directory’s filenames; use “**./&#42;.pdf**”.

Be careful about displaying or storing pathnames, since they can include newlines, tabs, escape (which can begin terminal controls), or sequences that are not legal strings. On some systems, merely displaying filenames can invoke terminal controls, which can then run commands with the privilege of the one displaying.