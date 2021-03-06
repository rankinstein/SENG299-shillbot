
import unittest
import codecs
import os

from workers.basic_worker import BasicUserParseWorker, WorkerException


class TestWorkerBasic(unittest.TestCase):

    def test_basic_worker_connection(self):
        """
        Purpose: Test regular running of worker
        Expectation: startup system, hit the reddit user and parse the data, fail to send to mothership (exception)

        :precondition: Mothership server not running
        :return:
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        # Can't connect to mother, so should raise ConnectionRefusedError, but should run everything else
        self.assertRaises(ConnectionRefusedError, worker.run)

    def test_worker_parsing(self):
        """
        Purpose: Test regular parsing mechanisms of worker
        Expectation: Load html file, send it to worker to parse, should return list of results

        :return:
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        file_path = '%s/%s' % (os.path.dirname(os.path.realpath(__file__)), 'test_resources/sample_GET_response.html')

        with codecs.open(file_path, encoding='utf-8') as f:
            text = f.read()

        results, next_page = worker.parse_text(str(text).strip().replace('\r\n', ''))

        self.assertGreater(len(results), 0)     # Check that results are returned
        self.assertEqual(len(results[0]), 3)    # Check that results are in triplets (check formatting)

    def test_worker_add_links_max_limit(self):
        worker = None
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        worker.max_links = 0
        len_to_crawl_before = len(worker.to_crawl)
        worker.add_links("test.com")
        len_to_crawl_after = len(worker.to_crawl)

        self.assertEqual(len_to_crawl_after, len_to_crawl_before)

        """
        New Unit tests added below
        """
    def test_worker_add_links_in_crawled(self):
        """
        calling add_links() with one link on a worker increases the to_crawl length by 1

        This unit test was partially implemented in class but was broken
        It is now fixed
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        worker.crawled = []

        len_to_crawl_before = len(worker.to_crawl)
        worker.add_links(["https://www.reddit.com/user/GallowBoob"])
        len_to_crawl_after = len(worker.to_crawl)

        self.assertEqual(len_to_crawl_after, len_to_crawl_before+1)

    def test_worker_cannot_add_duplicate_links(self):
        """
        calling add_links() with two identical links only adds 1 link
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        worker.crawled = []

        len_to_crawl_before = len(worker.to_crawl)
        worker.add_links([
            "https://www.reddit.com/user/GallowBoob",
            "https://www.reddit.com/user/GallowBoob"])
        len_to_crawl_after = len(worker.to_crawl)

        self.assertEqual(len_to_crawl_after, len_to_crawl_before+1)

    def test_worked_cannot_add_already_crawled_links(self):
        """
        adding a link that has already been crawled does not change the to_crawl length
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        worker.crawled = []

        len_to_crawl_before = len(worker.to_crawl)
        worker.add_links(["https://www.reddit.com/user/Chrikelnel"])
        len_to_crawl_after = len(worker.to_crawl)

        self.assertEqual(len_to_crawl_after, len_to_crawl_before+1)



