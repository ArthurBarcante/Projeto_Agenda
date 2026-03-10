from app.core.db.repositories import BaseRepository


class FakeSession:
    def __init__(self):
        self.added = []
        self.added_all = []
        self.committed = False
        self.flushed = False
        self.refreshed = []
        self.query_entities = None

    def add(self, instance):
        self.added.append(instance)

    def add_all(self, instances):
        self.added_all.extend(instances)

    def flush(self):
        self.flushed = True

    def commit(self):
        self.committed = True

    def refresh(self, instance):
        self.refreshed.append(instance)

    def query(self, *entities):
        self.query_entities = entities
        return entities


def test_query_delegates_to_session_query():
    db = FakeSession()
    repository = BaseRepository(db)

    entities = repository.query("model", "field")

    assert entities == ("model", "field")
    assert db.query_entities == ("model", "field")


def test_mutation_methods_delegate_to_session():
    db = FakeSession()
    repository = BaseRepository(db)

    item = {"id": 1}
    repository.add(item)
    repository.add_all([{"id": 2}, {"id": 3}])
    repository.flush()
    repository.commit()
    repository.refresh(item)

    assert db.added == [item]
    assert db.added_all == [{"id": 2}, {"id": 3}]
    assert db.flushed is True
    assert db.committed is True
    assert db.refreshed == [item]
