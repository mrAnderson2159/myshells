import tempfile
import unittest
from unittest.mock import mock_open, patch, MagicMock
from src.alias_manager import *
from click.testing import CliRunner


class TestAliasManager(unittest.TestCase):
    def setUp(self):
        self.test_alias_name = 'testalias'
        self.test_alias_body = 'echo Test'
        self.test_alias_line = f"alias {self.test_alias_name}='{self.test_alias_body}'\n"

    def test_build_alias(self):
        constructed_alias = build_alias(self.test_alias_name, self.test_alias_body)
        self.assertEqual(constructed_alias, self.test_alias_line)

    def test_list_aliases(self):
        # Simula il contenuto del file di configurazione della shell
        mock_file_content = 'alias ls="ls -la"\nalias ll="ls -l"\n'

        # Usa `mock_open` per simulare la funzione open e il suo comportamento
        mocked_open = mock_open(read_data=mock_file_content)

        # Usa `patch` per sostituire la funzione open con la nostra mock_open solo per questo test
        with patch('builtins.open', mocked_open):
            result = list_aliases()

        # Verifica che il contenuto restituito sia quello che ci aspettiamo
        self.assertEqual(result, ['alias ls="ls -la"\n', 'alias ll="ls -l"\n'])

    @patch('src.alias_manager.Path', autospec=True)
    def test_backup_cleaner_expanduser_called(self, mock_path_class):
        # Creiamo un mock per l'istanza di Path
        mock_path_instance = MagicMock(spec=Path)

        # Configuriamo il mock della classe Path per restituire il mock dell'istanza quando viene chiamato
        mock_path_class.return_value = mock_path_instance

        # Ora quando backup_cleaner chiama Path('some_path'), otterrà mock_path_instance
        backup_cleaner('test_source_file')

        # Verifichiamo che expanduser sia stato chiamato sul mock dell'istanza di Path
        mock_path_instance.expanduser.assert_called_once()

    @patch('src.alias_manager.Path', autospec=True)
    def test_backup_cleaner_expanduser_not_called(self, mock_path_class):
        # Creiamo un mock per l'istanza di Path
        mock_path_instance = MagicMock(spec=Path)

        # Configuriamo il mock della classe Path per restituire il mock dell'istanza quando viene chiamato
        mock_path_class.return_value = mock_path_instance

        # Ora quando backup_cleaner chiama Path('some_path'), otterrà mock_path_instance
        backup_cleaner(Path('test_source_file'))

        # Verifichiamo che expanduser sia stato chiamato sul mock dell'istanza di Path
        mock_path_instance.expanduser.assert_not_called()

    def test_backup_cleaner_with_success(self):
        # Crea una directory temporanea
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir = Path(tmp_dir)
            # Crea alcuni file di backup nella directory temporanea
            backup_files = [
                'test_source_file_20240101.backup',
                'test_source_file_20240102.backup',
                'test_source_file_20240103.backup',
                'test_source_file_20240104.backup',
                'test_source_file_20240105.backup'
            ]
            for filename in backup_files:
                open(tmp_dir / filename, 'w').close()

            # Aggiungi altri file non backup nella directory
            open(tmp_dir / 'test_source_file', 'w').close()
            open(tmp_dir / 'some_other_file.txt', 'w').close()

            # Chiama la funzione backup_cleaner con il percorso del file di test
            backup_cleaner(tmp_dir / 'test_source_file')

            # Verifica che solo i file di backup più vecchi siano stati eliminati
            remaining_files = set(os.listdir(tmp_dir))
            expected_remaining_files = {'test_source_file_20240105.backup', 'test_source_file_20240104.backup',
                                        'test_source_file_20240103.backup', 'test_source_file', 'some_other_file.txt'}
            self.assertEqual(expected_remaining_files, remaining_files)

    @patch('src.alias_manager.copyfile')
    @patch('src.alias_manager.strftime', return_value='20240401')
    @patch('src.alias_manager.backup_cleaner')
    def test_backup(self, mock_backup_cleaner, mock_strftime, mock_copyfile):
        # Simula il percorso del file sorgente e del file di backup
        source_file = 'test_source_file'
        expected_backup_file = f"{source_file}_20240401.backup"

        # Chiama la funzione di backup
        backup(source_file)

        # Verifica che copyfile sia stato chiamato con i percorsi giusti
        mock_copyfile.assert_called_once_with(source_file, expected_backup_file)

        # Verifica che strftime sia stato chiamato con il formato giusto
        mock_strftime.assert_called_once_with('%Y%m%d%H%M%S')

        # Verifica che strftime sia stato chiamato backup_cleaner
        mock_backup_cleaner.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_update(self, mocked_open):
        # Simula le linee che vogliamo scrivere nel file
        mock_lines = ['alias g="git"\n', 'alias ll="ls -la"\n']

        # Chiama la funzione di update
        update(mock_lines)

        # Verifica che la funzione open sia stata chiamata correttamente con il file di configurazione della shell e in modalità di scrittura
        mocked_open.assert_called_once_with(bash_profile(), 'w')

        # Ottiene l'handle del file mockato (il primo ed unico chiamato)
        file_handle = mocked_open()

        # Verifica che il contenuto scritto sia quello atteso
        file_handle.writelines.assert_called_once_with(mock_lines)

    def test_split_valid_alias(self):
        # Testa una definizione di alias valida
        alias_line = "alias ll='ls -la'"
        expected_result = ('ll', 'ls -la')
        actual_result = split_alias(alias_line)
        self.assertEqual(expected_result, actual_result)

    def test_split_valid_alias_with_double_quotes(self):
        # Testa una definizione di alias valida con doppi apici
        alias_line = 'alias ll="ls -la"'
        expected_result = ('ll', 'ls -la')
        actual_result = split_alias(alias_line)
        self.assertEqual(expected_result, actual_result)

    def test_split_alias_without_quotes(self):
        # Testa una definizione di alias senza apici
        alias_line = "alias ll=ls -la"
        expected_result = ('ll', 'ls -la')
        actual_result = split_alias(alias_line)
        self.assertEqual(expected_result, actual_result)

    def test_split_alias_with_additional_spaces(self):
        # Testa una definizione di alias con spazi aggiuntivi
        alias_line = "alias   ll  =  'ls -la'  "
        expected_result = ('ll', 'ls -la')
        actual_result = split_alias(alias_line)
        self.assertEqual(expected_result, actual_result)

    def test_split_invalid_alias(self):
        # Testa una definizione di alias non valida
        alias_line = "aliasll='ls -la'"
        with self.assertRaises(ValueError):
            split_alias(alias_line)

    def test_split_alias_missing_command(self):
        # Testa una definizione di alias mancante del comando
        alias_line = "alias ll="

        with self.assertRaises(ValueError):
            split_alias(alias_line)

    @patch('src.alias_manager.list_aliases')
    @patch('src.alias_manager.update')
    def test_modify_alias(self, mock_update, mock_list_aliases):
        mock_list_aliases.return_value = ['alias g="git status"\n', 'alias ll="ls -la"\n']
        # Aspettati che il nuovo comando dell'alias sia racchiuso tra apici singoli
        expected_lines = ['alias g="git status"\n', "alias ll='ls -lh'\n"]
        alias_data = {"line": 1, "body": "ls -la"}

        modify_alias(alias_name='ll', alias_data=alias_data, new_body='ls -lh')

        mock_update.assert_called_once_with(expected_lines)

    @patch('src.alias_manager.list_aliases')
    @patch('src.alias_manager.update')
    def test_rename_alias(self, mock_update, mock_list_aliases):
        mock_list_aliases.return_value = ['alias g="git status"\n', 'alias ll="ls -la"\n']
        expected_lines = ['alias g="git status"\n', "alias listall='ls -la'\n"]
        alias_data = {"line": 1, "body": "ls -la"}

        rename_alias(alias_data=alias_data, new_name='listall')

        mock_update.assert_called_once_with(expected_lines)


class TestGetAlias(unittest.TestCase):

    def setUp(self):
        # Alias e contenuti mock per il test
        self.alias_content = [
            "alias g='git'\n",
            "alias ls='ls --color=auto'\n",
            "alias ll='ls -la'\n",
            # Alias ridefinito per testare l'ottenimento dell'ultima definizione
            "alias g='git status'\n"
        ]

    @patch('src.alias_manager.list_aliases')
    def test_get_existing_alias(self, mock_list_aliases):
        # Simula il ritorno del contenuto mock quando si chiama list_aliases
        mock_list_aliases.return_value = self.alias_content

        # Chiama get_alias per un alias esistente
        result = get_alias('g')

        # Verifica che l'ultima definizione dell'alias sia stata restituita
        self.assertEqual(result, {'line': 3, 'body': 'git status'})

    @patch('src.alias_manager.list_aliases')
    def test_get_non_existing_alias(self, mock_list_aliases):
        # Simula il ritorno del contenuto mock quando si chiama list_aliases
        mock_list_aliases.return_value = self.alias_content

        # Verifica che la funzione sollevi AliasNotFoundError per un alias non esistente
        with self.assertRaises(AliasNotFoundError):
            get_alias('nonexistent')

    @patch('src.alias_manager.list_aliases')
    def test_get_alias_with_invalid_format(self, mock_list_aliases):
        # Aggiungi un alias con un formato non valido al contenuto mock
        mock_list_aliases.return_value = self.alias_content + ["alias badalias"]

        # Verifica che la funzione sollevi un'eccezione per un alias con formato non valido
        with self.assertRaises(AliasNotFoundError):
            get_alias('badalias')


class TestNewAliasCommand(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    # @patch('src.alias_manager.get_alias', side_effect=AliasNotFoundError)
    #     Questa patch modifica temporaneamente il comportamento della funzione get_alias all'interno del modulo src.alias_manager durante l'esecuzione di questo test specifico.
    #     Il parametro side_effect=AliasNotFoundError indica che ogni volta che get_alias viene chiamata durante il test, invece di eseguire la sua logica normale, solleverà un'eccezione AliasNotFoundError.
    #     Ciò simula uno scenario in cui la funzione get_alias non riesce a trovare l'alias richiesto, un aspetto chiave per testare l'aggiunta di un nuovo alias.
    # @patch('builtins.open', new_callable=mock_open)
    #     Questa patch sostituisce la funzione integrata open con una versione mock (simulata) che non opera su file reali. Questo è fondamentale per prevenire modifiche ai file reali sul sistema durante l'esecuzione del test.
    #     new_callable=mock_open specifica che la funzione mockizzata dovrebbe comportarsi come la funzione open, permettendo di simularne il comportamento come l'apertura di un file e la scrittura su di esso.
    #     Questo approccio permette di verificare che il file di configurazione venga aperto e modificato come previsto, senza però influenzare il file reale.
    # @patch('src.alias_manager.backup')
    #     Questa patch modifica temporaneamente la funzione backup nel modulo src.alias_manager, sostituendola con una versione mock durante il test.
    #     L'assenza di parametri aggiuntivi oltre al percorso della funzione indica che il test non si aspetta effetti secondari specifici dalla funzione backup, ma vuole solo assicurarsi che venga chiamata in un certo punto del flusso di esecuzione.
    #     L'utilizzo di questa patch consente di verificare che venga eseguito un backup prima di apportare modifiche al file di configurazione, senza però creare backup reali nel file system durante il test.
    @patch('src.alias_manager.get_alias', side_effect=AliasNotFoundError)
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.alias_manager.backup')
    def test_new_alias_success_no_overwrite(self, mock_backup, mock_file, mock_get_alias):
        # Esegue il comando 'newalias' con un nuovo alias per verificare il flusso di successo
        result = self.runner.invoke(newalias, ['testalias', 'echo', 'Hello, World!'])

        # Verifica che la funzione get_alias sia stata chiamata una volta con il nome dell'alias
        # per controllare se l'alias esiste già
        mock_get_alias.assert_called_once_with('testalias')

        # Verifica che la funzione di backup sia stata chiamata una volta
        # per creare una copia di sicurezza del file di configurazione prima di modificarlo
        mock_backup.assert_called_once()

        # Verifica che la funzione open sia stata chiamata una volta con il file di configurazione
        # della shell in modalità di append per aggiungere il nuovo alias
        mock_file.assert_called_once_with(bash_profile(), 'a')

        # Ottiene l'handle del file mockato e verifica che la scrittura dell'alias
        # nel file sia stata effettuata correttamente
        file_handle = mock_file()
        file_handle.write.assert_called_once_with("alias testalias='echo Hello, World!'\n")

        # Verifica che il codice di uscita del comando sia 0, indicando un'esecuzione riuscita
        self.assertEqual(result.exit_code, 0)

        # Verifica che l'output del comando contenga il messaggio di successo previsto
        self.assertIn("Alias testalias added successfully.", result.output)

    @patch('src.alias_manager.get_alias')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.alias_manager.backup')
    def test_new_alias_success_with_overwrite(self, mock_backup, mock_file, mock_get_alias):
        mock_get_alias.return_value = {"line": 10, "body": "previous command"}
        with patch('click.confirm', return_value=True):
            result = self.runner.invoke(newalias, ['testalias', 'echo', 'New command!'])
            mock_get_alias.assert_called_once_with('testalias')
            mock_backup.assert_called_once()
            mock_file.assert_called_once_with(bash_profile(), 'a')
            file_handle = mock_file()
            file_handle.write.assert_called_once_with("alias testalias='echo New command!'\n")
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Alias testalias updated successfully.", result.output)

    @patch('src.alias_manager.get_alias')
    @patch('builtins.open', new_callable=mock_open)
    def test_new_alias_cancel_overwrite(self, mock_file, mock_get_alias):
        mock_get_alias.return_value = {"line": 10, "body": "previous command"}
        with patch('click.confirm', return_value=False):
            result = self.runner.invoke(newalias, ['testalias', 'echo', 'New command!'])
            mock_get_alias.assert_called_once_with('testalias')
            mock_file.assert_not_called()
            self.assertEqual(result.exit_code, 0)
            self.assertIn("No changes made.", result.output)

    @patch('src.alias_manager.get_alias', side_effect=AliasNotFoundError)
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.alias_manager.backup', side_effect=IOError("Failed to backup"))
    def test_new_alias_backup_failure(self, mock_backup, mock_file, mock_get_alias):
        result = self.runner.invoke(newalias, ['testalias', 'echo', 'Hello, World!'])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Error: Failed to write to", result.output)


class TestMvalias(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch('src.alias_manager.get_alias', return_value={"line": 1, "body": "old_command"})
    @patch('src.alias_manager.backup')
    @patch('src.alias_manager.rename_alias')
    def test_rename_alias(self, mock_rename, mock_backup, mock_get):
        with patch('click.confirm', return_value=True):
            result = self.runner.invoke(mvalias, ['old_alias', '--name', 'new_alias'])
            mock_get.assert_called_once_with('old_alias')
            mock_backup.assert_called_once()
            mock_rename.assert_called_once_with({"line": 1, "body": "old_command"}, new_name='new_alias')
            self.assertEqual(result.exit_code, 0)
            self.assertIn("\nAlias old_alias successfully renamed to new_alias\n", result.output)

    @patch('src.alias_manager.get_alias', return_value={"line": 1, "body": "old_command"})
    @patch('src.alias_manager.backup')
    @patch('src.alias_manager.modify_alias')
    def test_modify_alias_command(self, mock_modify, mock_backup, mock_get):
        with patch('click.confirm', return_value=True):
            result = self.runner.invoke(mvalias, ['alias_name', 'new_command'])
            mock_get.assert_called_once_with('alias_name')
            mock_backup.assert_called_once()
            mock_modify.assert_called_once_with({"line": 1, "body": "old_command"}, new_body='new_command')
            self.assertEqual(result.exit_code, 0)
            self.assertIn("\nNew alias: alias_name -> new_command\nSuccessfully created\n\n", result.output)

    @patch('src.alias_manager.get_alias', side_effect=AliasNotFoundError)
    def test_alias_not_found_error(self, mock_get):
        result = self.runner.invoke(mvalias, ['nonexistent_alias', 'new_command'])
        mock_get.assert_called_once_with('nonexistent_alias')
        self.assertEqual(result.exit_code, 0)  # or another appropriate exit code for error
        self.assertIn("Error: Alias nonexistent_alias not found.", result.output)


class TestRmalias(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch('src.alias_manager.list_aliases')
    @patch('src.alias_manager.update')
    def test_remove_existing_alias(self, mock_update, mock_list_aliases):
        with patch('click.confirm', return_value=True):
            # Simula il contenuto del file di configurazione contenente l'alias da rimuovere
            mock_list_aliases.return_value = ['alias ls="ls -la"\n', 'alias ll="ls -l"\n']

            # Esegue il comando rmalias per rimuovere l'alias 'll'
            result = self.runner.invoke(rmalias, ['ll'])

            # Verifica che il file di configurazione sia stato aggiornato senza l'alias 'll'
            mock_update.assert_called_once_with(['alias ls="ls -la"\n'])

            # Verifica che il comando sia terminato con successo
            self.assertEqual(result.exit_code, 0)

            # Verifica che l'output del comando indichi la rimozione avvenuta con successo
            self.assertIn("Alias ll has been successfully deleted.", result.output)

    @patch('src.alias_manager.list_aliases')
    @patch('src.alias_manager.update')
    def test_remove_non_existing_alias(self, mock_update, mock_list_aliases):
        # Simula il contenuto del file di configurazione senza l'alias da rimuovere
        mock_list_aliases.return_value = ['alias ls="ls -la"\n', 'alias ll="ls -l"\n']

        # Esegue il comando rmalias per tentare di rimuovere un alias non esistente
        result = self.runner.invoke(rmalias, ['nonexistent'])

        # Verifica che la funzione di aggiornamento non sia stata chiamata, poiché non ci sono modifiche da applicare
        mock_update.assert_not_called()

        # Verifica che il comando sia terminato con successo (o con un codice di errore specifico, se preferisci)
        self.assertEqual(result.exit_code, 0)  # o un altro codice di uscita appropriato

        # Verifica che l'output del comando informi l'utente che l'alias non è stato trovato
        self.assertIn("Alias nonexistent was not found.", result.output)

    @patch('src.alias_manager.list_aliases')
    @patch('src.alias_manager.update')
    def test_remove_multiple_aliases(self, mock_update, mock_list_aliases):
        with patch('click.confirm', return_value=True):
            # Simula il contenuto del file di configurazione contenente gli alias da rimuovere
            mock_list_aliases.return_value = [
                'alias ls="ls -la"\n',
                'alias ll="ls -l"\n',
                'alias g="git"\n',
                'alias ga="git add"\n'
            ]

            # Esegue il comando rmalias per rimuovere gli alias 'll' e 'ga'
            result = self.runner.invoke(rmalias, ['ll', 'ga'])

            # Verifica che il file di configurazione sia stato aggiornato senza gli alias 'll' e 'ga'
            mock_update.assert_called_once_with([
                'alias ls="ls -la"\n',
                'alias g="git"\n'
            ])

            # Verifica che il comando sia terminato con successo
            self.assertEqual(result.exit_code, 0)

            # Verifica che l'output del comando indichi la rimozione avvenuta con successo
            self.assertIn("Alias ll has been successfully deleted.", result.output)
            self.assertIn("Alias ga has been successfully deleted.", result.output)

            # Verifica che venga creato un backup prima della rimozione
            self.assertIn("Backup of the original aliases file created", result.output)

            # Verifica che il file delle alias sia stato aggiornato
            self.assertIn("The aliases file has been updated.", result.output)


if __name__ == '__main__':
    unittest.main()
