If the field type of a PrimaryKey or SecondaryKey is a composite key class containing more than one key field, then a KeyField annotation must be present on each non-transient instance field of the composite key class. The KeyField value must be a number between one and the number of non-transient instance fields declared in the composite key class.

Note that a composite key class is a flat container for one or more simple type fields. All non-transient instance fields in the composite key class are key fields, and its superclass must be Object.

For example:

  @Entity
  class Animal {
      @PrimaryKey
      Classification classification;
      ...
  }

  @Persistent
  class Classification {
      @KeyField(1) String kingdom;
      @KeyField(2) String phylum;
      @KeyField(3) String clazz;
      @KeyField(4) String order;
      @KeyField(5) String family;
      @KeyField(6) String genus;
      @KeyField(7) String species;
      @KeyField(8) String subspecies;
      ...
  }
This causes entities to be sorted first by kingdom, then by phylum within kingdom, and so on.

The fields in a composite key class may not be null.