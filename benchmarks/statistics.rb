module Utilities

  module Statistics
    extend self

    class NotEnoughElements < StandardError; end

    # ================================================================
    # "spreadsheet functions" in name and behavior

    def min(array)
      raise NotEnoughElements.new("need one or more elements") unless array.count > 0
      array.min
    end

    def max(array)
      raise NotEnoughElements.new("need one or more elements") unless array.count > 0
      array.max
    end

    def mean(array)
      raise NotEnoughElements.new("need one or more elements") unless array.count > 0
      sum = array.reduce(0.0) {|m, v| m+v}
      (sum / array.count.to_f)
    end

    def median(array, sorted = false)
      raise NotEnoughElements.new("need one or more elements") unless array.count > 0
      (array.count == 1) ? array[0] : _quantile(array, 0.5, sorted)
    end

    def var(array)
      raise NotEnoughElements.new("need one or more elements") unless array.count > 0
      _variance(array, true)
    end

    def varp(array)
      raise NotEnoughElements.new("need one or more elements") unless array.count > 1
      _variance(array, false)
    end

    def stdev(array)
      Math.sqrt(var(array))
    end

    def stdevp(array)
      Math.sqrt(varp(array))
    end

    def rank(val, array)
      array = array.sort.uniq
      index = array.index(val)
      return nil || array.size - index
    end

    def percentile(array, p)
      raise NotEnoughElements.new("need one or more elements") unless array.count > 0
      _quantile(array, p, false)
    end
      
    # ================================================================
    # argument checked functions

    def variance(array, bias_corrected = true, mean = nil)
      raise NotEnoughElements.new("need one or more elements") unless array.count > (bias_corrected ? 0 : 1)
      _variance(array, bias_corrected, mean)
    end

    def sd(array, bias_corrected = true, mean = nil)
      Math.sqrt(variance(array, bias_corrected, mean))
    end

    def quantile(array, p, sorted = false)
      raise NotEnoughElements.new("need one or more elements") unless array.count > 0
      _quantile(array, p, sorted)
    end

    # ================================================================
    # unchecked versions

    def _variance(array, bias_corrected = true, mean = nil)
      n = array.length
      mean ||= mean(array)
      array.inject(0) {|accum, x| accum + (x-mean)**2 } / (bias_corrected ? (n - 1) : n)
    end

    def _quantile(array, p, sorted)
      array = array.sort unless sorted
      return array[-1].to_f if p == 1.0
      rank = p * (array.length - 1.0) # 0.0 <= p < 1.0  =>  0.0 <= rank < (len-1)
      lrank = rank.floor              # integer part of rank
      d = rank - lrank                # fractional part of rank
      lerp(d, 0.0, 1.0, array[lrank], array[lrank+1])
    end
    
    # a handy method to have around...
    def summarize(array, sorted = false)
      array = array.sort unless sorted
      mean = mean(array)
      {
        :count => array.size,
        :minimum => array.first,
        :maximum => array.last,
        :mean => mean,
        :median => median(array, true),
        :standard_deviation => sd(array, true, mean)
      }
    end
    
    # Rank an item against an array of values.  
    #
    # Return two values: the rank of the item and the 
    # number of distinct values in the array.
    #
    def ranking(values, item)
      # puts("=== ranking: #{values}, #{item}")
      return nil if item.nil?
      values = values.append(item).sort.uniq
      [values.index(item)+1, values.count]
    end

    def lerp(x, x0, x1, y0, y1)
      y0 + (x - x0) * (y1 - y0) / (x1 - x0)
    end

    def percentile_value(items, percentile)
      items = items.sort
      index = (items.size * percentile).floor
      items[index]
    end

    def weighted_average(values, weights)
      tot_v = 0.0
      tot_w = 0.0
      values.each_with_index do |v, i|
        w = weights[i]
        tot_v += v * w
        tot_w += w
      end
      (tot_w != 0.0) ? tot_v / tot_w : Float::INFINITY
    end

  end

end
