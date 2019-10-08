library(xlsx)

remap_df <- read.xlsx("kg2-edge-labels-stats-annotated.xlsx",
                      sheetIndex=1,
                      header=TRUE,
                      stringsAsFactors=FALSE)

with(remap_df,
{
    inds_bad <- which(Propose. != "delete" &
                      is.na(Proposed.official.KG2.CURIE.ID.))
    print("The following CURIEs are missing remap data:")
    print(Predicate.CURIE.in..raw..KG2.graph.[inds_bad])

    inds_not_unique <- which(table(Predicate.CURIE.in..raw..KG2.graph.) > 1)
    print("The following CURIEs are not unique in the input table:")
    print(Predicate.CURIE.in..raw..KG2.graph.[inds_not_unique])
#    stopifnot(Propose. == "delete" |
#              ! is.na(Proposed.official.KG2.CURIE.ID.))


    inds_bad <- which(Propose. == "keep" &
                      Predicate.CURIE.in..raw..KG2.graph. != Proposed.official.KG2.CURIE.ID.)
    print("The following CURIEs are marked keep, but with a proposed change in the CURIE:")
    print(Predicate.CURIE.in..raw..KG2.graph.[inds_bad])

    inds_bad <- which(Propose. != "keep" &
                      Predicate.CURIE.in..raw..KG2.graph. == Proposed.official.KG2.CURIE.ID.)
    print("The following CURIEs are marked to be changed, but but new CURIE is the same:")
    print(Predicate.CURIE.in..raw..KG2.graph.[inds_bad])

    curie_prefixes <- sapply(strsplit(Predicate.CURIE.in..raw..KG2.graph., ":"), "[[", 1)

    keys <- paste(curie_prefixes, count..., sep="")

    curie_checks <- sapply(unique(keys), function(unique_key) {
        inds <- which(keys == unique_key)
        length(inds) > 10 & all(Propose.[inds] != "delete")
    })
    print("CURIE prefix pairs with identical counts for which neither is delete:")
    print(curie_checks[curie_checks])

    checks <- sapply(unique(Edge.label.in..raw..KG2.graph.), function(unique_edge_label) {
        inds <- which(Edge.label.in..raw..KG2.graph. == unique_edge_label)

        length(inds) > 1 & length(unique(Proposed.official.KG2.CURIE.ID.[inds])) > 1
    })
    print("edge labels for which there are non-identical mapped CURIEs: ")
    print(checks[checks])
    
})

## - any two rows with the same value for column C should be identical in column F
## - warn for any two rows with identical counts and identical curie prefixes, for which neither is "delete"

